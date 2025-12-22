"""
AWS Athena Setup Module
Creates and configures Athena tables and partitions
"""

import logging
import sys
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
import time

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class AthenaSetup:
    """Setup and configure AWS Athena tables and partitions"""

    def __init__(self):
        self.config = config
        self.athena_client = boto3.client(
            "athena",
            region_name=self.config.aws_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )
        self.glue_client = boto3.client(
            "glue",
            region_name=self.config.aws_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )

    def execute_query(self, query: str, wait_for_completion: bool = True) -> Dict[str, Any]:
        """
        Execute an Athena query

        Args:
            query: SQL query to execute
            wait_for_completion: Wait for query to complete

        Returns:
            Query execution details
        """
        try:
            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": self.config.athena_database},
                ResultConfiguration={
                    "OutputLocation": f"s3://{self.config.s3_athena_results_bucket}/query-results/"
                },
                WorkGroup=self.config.athena_workgroup,
            )

            query_execution_id = response["QueryExecutionId"]
            logger.info(f"Query started with ID: {query_execution_id}")

            if wait_for_completion:
                return self.wait_for_query(query_execution_id)
            else:
                return {"QueryExecutionId": query_execution_id, "Status": "RUNNING"}

        except ClientError as e:
            logger.error(f"Failed to execute query: {e}")
            raise

    def wait_for_query(self, query_execution_id: str, max_wait: int = 300) -> Dict[str, Any]:
        """
        Wait for query to complete

        Args:
            query_execution_id: Query execution ID
            max_wait: Maximum wait time in seconds

        Returns:
            Query execution details
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            response = self.athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )

            status = response["QueryExecution"]["Status"]["State"]

            if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                logger.info(f"Query {query_execution_id} completed with status: {status}")
                return response["QueryExecution"]

            time.sleep(2)

        raise TimeoutError(f"Query {query_execution_id} did not complete within {max_wait}s")

    def create_database(self) -> bool:
        """Create Athena database if it doesn't exist"""
        query = f"""
        CREATE DATABASE IF NOT EXISTS {self.config.athena_database}
        COMMENT 'Tokyo-IA Analytics Database'
        LOCATION 's3://{self.config.s3_data_lake_bucket}/'
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info(f"Database {self.config.athena_database} created successfully")
                return True
            else:
                logger.error(f"Failed to create database: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return False

    def create_workflows_table(self) -> bool:
        """Create workflows table in Athena"""
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {self.config.athena_database}.workflows (
            id STRING,
            name STRING,
            description STRING,
            status STRING,
            workflow_type STRING,
            initiator STRING,
            total_tasks INT,
            completed_tasks INT,
            failed_tasks INT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            duration_ms INT,
            total_tokens_used INT,
            total_cost_usd DECIMAL(10,6),
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata STRING
        )
        PARTITIONED BY (year INT, month INT, day INT)
        STORED AS PARQUET
        LOCATION 's3://{self.config.s3_data_lake_bucket}/workflows/'
        TBLPROPERTIES ('parquet.compression'='SNAPPY')
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info("Workflows table created successfully")
                return True
            else:
                logger.error(f"Failed to create workflows table: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating workflows table: {e}")
            return False

    def create_agent_tasks_table(self) -> bool:
        """Create agent_tasks table in Athena"""
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {self.config.athena_database}.agent_tasks (
            id STRING,
            agent_id STRING,
            workflow_id STRING,
            task_type STRING,
            description STRING,
            status STRING,
            input_data STRING,
            output_data STRING,
            error_message STRING,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            duration_ms INT,
            tokens_used INT,
            cost_usd DECIMAL(10,6),
            retry_count INT,
            parent_task_id STRING,
            created_at TIMESTAMP,
            metadata STRING
        )
        PARTITIONED BY (year INT, month INT, day INT)
        STORED AS PARQUET
        LOCATION 's3://{self.config.s3_data_lake_bucket}/agent_tasks/'
        TBLPROPERTIES ('parquet.compression'='SNAPPY')
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info("Agent tasks table created successfully")
                return True
            else:
                logger.error(f"Failed to create agent_tasks table: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating agent_tasks table: {e}")
            return False

    def create_agent_metrics_table(self) -> bool:
        """Create agent_metrics table in Athena"""
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {self.config.athena_database}.agent_metrics (
            id STRING,
            agent_id STRING,
            metric_type STRING,
            metric_value DOUBLE,
            metric_unit STRING,
            recorded_at TIMESTAMP,
            context STRING
        )
        PARTITIONED BY (year INT, month INT, day INT)
        STORED AS PARQUET
        LOCATION 's3://{self.config.s3_data_lake_bucket}/agent_metrics/'
        TBLPROPERTIES ('parquet.compression'='SNAPPY')
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info("Agent metrics table created successfully")
                return True
            else:
                logger.error(f"Failed to create agent_metrics table: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating agent_metrics table: {e}")
            return False

    def create_agent_interactions_table(self) -> bool:
        """Create agent_interactions table in Athena"""
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {self.config.athena_database}.agent_interactions (
            id STRING,
            workflow_id STRING,
            from_agent_id STRING,
            to_agent_id STRING,
            interaction_type STRING,
            message STRING,
            payload STRING,
            created_at TIMESTAMP
        )
        PARTITIONED BY (year INT, month INT, day INT)
        STORED AS PARQUET
        LOCATION 's3://{self.config.s3_data_lake_bucket}/agent_interactions/'
        TBLPROPERTIES ('parquet.compression'='SNAPPY')
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info("Agent interactions table created successfully")
                return True
            else:
                logger.error(f"Failed to create agent_interactions table: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating agent_interactions table: {e}")
            return False

    def create_user_sessions_table(self) -> bool:
        """Create user_sessions table in Athena"""
        query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {self.config.athena_database}.user_sessions (
            id STRING,
            user_id STRING,
            session_token STRING,
            device_info STRING,
            ip_address STRING,
            started_at TIMESTAMP,
            last_activity_at TIMESTAMP,
            ended_at TIMESTAMP,
            is_active BOOLEAN,
            metadata STRING
        )
        PARTITIONED BY (year INT, month INT, day INT)
        STORED AS PARQUET
        LOCATION 's3://{self.config.s3_data_lake_bucket}/user_sessions/'
        TBLPROPERTIES ('parquet.compression'='SNAPPY')
        """

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info("User sessions table created successfully")
                return True
            else:
                logger.error(f"Failed to create user_sessions table: {result}")
                return False
        except Exception as e:
            logger.error(f"Error creating user_sessions table: {e}")
            return False

    def repair_partitions(self, table_name: str) -> bool:
        """
        Repair table partitions (discover new partitions in S3)

        Args:
            table_name: Name of the table to repair

        Returns:
            True if successful
        """
        query = f"MSCK REPAIR TABLE {self.config.athena_database}.{table_name}"

        try:
            result = self.execute_query(query)
            if result["Status"]["State"] == "SUCCEEDED":
                logger.info(f"Partitions repaired for {table_name}")
                return True
            else:
                logger.error(f"Failed to repair partitions: {result}")
                return False
        except Exception as e:
            logger.error(f"Error repairing partitions: {e}")
            return False

    def setup_all_tables(self) -> Dict[str, bool]:
        """
        Create all tables and repair partitions

        Returns:
            Dictionary with status for each operation
        """
        results = {}

        # Create database
        results["database"] = self.create_database()

        # Create tables
        results["workflows"] = self.create_workflows_table()
        results["agent_tasks"] = self.create_agent_tasks_table()
        results["agent_metrics"] = self.create_agent_metrics_table()
        results["agent_interactions"] = self.create_agent_interactions_table()
        results["user_sessions"] = self.create_user_sessions_table()

        # Repair partitions for all tables
        tables = ["workflows", "agent_tasks", "agent_metrics", "agent_interactions", "user_sessions"]
        for table in tables:
            results[f"{table}_partitions"] = self.repair_partitions(table)

        return results


def main():
    """Main entry point for Athena setup"""
    logger.info("Starting Athena setup...")

    setup = AthenaSetup()
    results = setup.setup_all_tables()

    # Print summary
    print("\n=== Athena Setup Summary ===")
    for operation, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {operation}")

    # Exit with error if any operations failed
    if not all(results.values()):
        sys.exit(1)

    logger.info("Athena setup completed successfully!")


if __name__ == "__main__":
    main()
