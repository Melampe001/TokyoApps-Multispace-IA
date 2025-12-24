#!/usr/bin/env python3
"""Setup Athena tables and partitions"""

import logging
import sys
from typing import List

import boto3
from botocore.exceptions import ClientError

from config import ATHENA_CONFIG, S3_CONFIG, TABLES_TO_EXPORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AthenaSetup:
    """Setup and manage Athena tables"""
    
    def __init__(self):
        """Initialize Athena clients"""
        self.athena_client = boto3.client('athena', region_name=S3_CONFIG['region'])
        self.glue_client = boto3.client('glue', region_name=S3_CONFIG['region'])
    
    def create_database(self) -> bool:
        """Create Athena database if it doesn't exist"""
        database = ATHENA_CONFIG['database']
        
        query = f"CREATE DATABASE IF NOT EXISTS {database}"
        
        try:
            logger.info(f"Creating database: {database}")
            self._execute_query(query)
            logger.info(f"Database '{database}' is ready")
            return True
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
            return False
    
    def create_table(self, table_name: str) -> bool:
        """
        Create Athena table with partition projection
        
        Args:
            table_name: Name of the table to create
            
        Returns:
            True if successful
        """
        logger.info(f"Creating table: {table_name}")
        
        # Get table schema based on table name
        schema = self._get_table_schema(table_name)
        
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {ATHENA_CONFIG['database']}.{table_name} (
            {schema}
        )
        PARTITIONED BY (
            year INT,
            month INT,
            day INT
        )
        STORED AS PARQUET
        LOCATION 's3://{S3_CONFIG['bucket']}/{S3_CONFIG['prefix']}/{table_name}/'
        TBLPROPERTIES (
            'parquet.compression'='SNAPPY',
            'projection.enabled'='true',
            'projection.year.type'='integer',
            'projection.year.range'='2020,2030',
            'projection.month.type'='integer',
            'projection.month.range'='1,12',
            'projection.day.type'='integer',
            'projection.day.range'='1,31',
            'storage.location.template'='s3://{S3_CONFIG['bucket']}/{S3_CONFIG['prefix']}/{table_name}/year=${{year}}/month=${{month}}/day=${{day}}'
        )
        """
        
        try:
            self._execute_query(query)
            logger.info(f"Table '{table_name}' created successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create table '{table_name}': {e}")
            return False
    
    def _get_table_schema(self, table_name: str) -> str:
        """Get schema definition for a table"""
        schemas = {
            'invoices': """
                invoice_id STRING,
                user_id STRING,
                amount DECIMAL(10,2),
                currency STRING,
                status STRING,
                product_id STRING,
                product_name STRING,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                metadata STRING
            """,
            'transactions': """
                transaction_id STRING,
                invoice_id STRING,
                user_id STRING,
                amount DECIMAL(10,2),
                currency STRING,
                payment_method STRING,
                status STRING,
                created_at TIMESTAMP,
                metadata STRING
            """,
            'users': """
                user_id STRING,
                email STRING,
                name STRING,
                status STRING,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                metadata STRING
            """,
            'subscriptions': """
                subscription_id STRING,
                user_id STRING,
                plan_id STRING,
                plan_name STRING,
                status STRING,
                price DECIMAL(10,2),
                currency STRING,
                billing_cycle STRING,
                started_at TIMESTAMP,
                ended_at TIMESTAMP,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                metadata STRING
            """
        }
        
        return schemas.get(table_name, "id STRING, data STRING")
    
    def repair_partitions(self, table_name: str) -> bool:
        """
        Repair table partitions (MSCK REPAIR TABLE)
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if successful
        """
        logger.info(f"Repairing partitions for table: {table_name}")
        
        query = f"MSCK REPAIR TABLE {ATHENA_CONFIG['database']}.{table_name}"
        
        try:
            self._execute_query(query)
            logger.info(f"Partitions repaired for '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to repair partitions for '{table_name}': {e}")
            return False
    
    def validate_table(self, table_name: str) -> bool:
        """
        Validate table by running a simple query
        
        Args:
            table_name: Name of the table to validate
            
        Returns:
            True if table is accessible
        """
        logger.info(f"Validating table: {table_name}")
        
        query = f"SELECT COUNT(*) as row_count FROM {ATHENA_CONFIG['database']}.{table_name} LIMIT 1"
        
        try:
            self._execute_query(query)
            logger.info(f"Table '{table_name}' is valid and accessible")
            return True
        except Exception as e:
            logger.error(f"Table validation failed for '{table_name}': {e}")
            return False
    
    def _execute_query(self, query: str) -> str:
        """
        Execute Athena query and wait for completion
        
        Args:
            query: SQL query to execute
            
        Returns:
            Query execution ID
        """
        try:
            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={
                    'Database': ATHENA_CONFIG['database']
                },
                ResultConfiguration={
                    'OutputLocation': ATHENA_CONFIG['output_location']
                },
                WorkGroup=ATHENA_CONFIG['workgroup']
            )
            
            query_execution_id = response['QueryExecutionId']
            
            # Wait for query to complete
            self._wait_for_query(query_execution_id)
            
            return query_execution_id
            
        except ClientError as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def _wait_for_query(self, query_execution_id: str, max_wait: int = 30):
        """
        Wait for query to complete
        
        Args:
            query_execution_id: Query execution ID
            max_wait: Maximum seconds to wait
        """
        import time
        
        for _ in range(max_wait):
            response = self.athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            
            state = response['QueryExecution']['Status']['State']
            
            if state == 'SUCCEEDED':
                return
            elif state in ['FAILED', 'CANCELLED']:
                reason = response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown')
                raise Exception(f"Query failed: {reason}")
            
            time.sleep(1)
        
        raise Exception(f"Query timed out after {max_wait} seconds")
    
    def setup_all_tables(self) -> bool:
        """Setup all tables"""
        # Create database
        if not self.create_database():
            return False
        
        # Create all tables
        results = []
        for table in TABLES_TO_EXPORT:
            success = self.create_table(table)
            results.append(success)
        
        all_success = all(results)
        
        if all_success:
            logger.info("All tables setup successfully")
        else:
            logger.error("Some tables failed to setup")
        
        return all_success


def main():
    """Main entry point"""
    setup = AthenaSetup()
    
    logger.info("Starting Athena setup...")
    
    success = setup.setup_all_tables()
    
    if success:
        logger.info("Athena setup completed successfully")
        sys.exit(0)
    else:
        logger.error("Athena setup failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
