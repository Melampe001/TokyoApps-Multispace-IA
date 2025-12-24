#!/usr/bin/env python3
"""Export PostgreSQL tables to S3 in Parquet format for Athena"""

import argparse
import io
import logging
import sys
from datetime import datetime, timedelta
from typing import Optional

import boto3
import pandas as pd
import psycopg2
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.exceptions import ClientError

from config import POSTGRES_CONFIG, S3_CONFIG, ATHENA_CONFIG, TABLES_TO_EXPORT, PARQUET_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PostgresToS3Exporter:
    """Export PostgreSQL tables to S3 in Parquet format"""
    
    def __init__(self, export_date: Optional[datetime] = None):
        """Initialize exporter with optional export date"""
        self.export_date = export_date or (datetime.now() - timedelta(days=1))
        self.s3_client = boto3.client('s3', region_name=S3_CONFIG['region'])
        
    def connect_postgres(self):
        """Establish PostgreSQL connection"""
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            logger.info("Successfully connected to PostgreSQL")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def export_table(self, table_name: str, mode: str = 'incremental') -> bool:
        """
        Export a table to S3 in Parquet format
        
        Args:
            table_name: Name of the table to export
            mode: 'incremental' or 'full' export
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Starting export of table '{table_name}' in {mode} mode")
        
        try:
            # Connect to PostgreSQL
            conn = self.connect_postgres()
            
            # Build query based on mode
            if mode == 'incremental':
                query = self._build_incremental_query(table_name)
            else:
                query = f"SELECT * FROM {table_name}"
            
            logger.info(f"Executing query: {query[:100]}...")
            
            # Read data into pandas DataFrame
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                logger.warning(f"No data found for table '{table_name}' on {self.export_date.date()}")
                return True
            
            # Add partition columns
            df['year'] = self.export_date.year
            df['month'] = self.export_date.month
            df['day'] = self.export_date.day
            
            # Upload to S3
            s3_key = self._generate_s3_key(table_name)
            self._upload_to_s3(df, s3_key)
            
            logger.info(f"Successfully exported {len(df)} rows from '{table_name}' to {s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export table '{table_name}': {e}")
            return False
    
    def _build_incremental_query(self, table_name: str) -> str:
        """Build query for incremental export"""
        date_str = self.export_date.strftime('%Y-%m-%d')
        return f"""
            SELECT * FROM {table_name}
            WHERE DATE(created_at) = '{date_str}'
        """
    
    def _generate_s3_key(self, table_name: str) -> str:
        """Generate S3 key with partitioning"""
        return (
            f"{S3_CONFIG['prefix']}/{table_name}/"
            f"year={self.export_date.year}/"
            f"month={self.export_date.month:02d}/"
            f"day={self.export_date.day:02d}/"
            f"{table_name}_{self.export_date.strftime('%Y%m%d')}.parquet"
        )
    
    def _upload_to_s3(self, df: pd.DataFrame, s3_key: str, retries: int = 3):
        """
        Upload DataFrame to S3 as Parquet with retry logic
        
        Args:
            df: DataFrame to upload
            s3_key: S3 key (path)
            retries: Number of retry attempts
        """
        table = pa.Table.from_pandas(df)
        
        for attempt in range(retries):
            try:
                # Write to parquet in memory
                buffer = io.BytesIO()
                pq.write_table(
                    table,
                    buffer,
                    compression=PARQUET_CONFIG['compression'],
                    row_group_size=PARQUET_CONFIG['row_group_size']
                )
                buffer.seek(0)
                
                # Upload to S3
                self.s3_client.put_object(
                    Bucket=S3_CONFIG['bucket'],
                    Key=s3_key,
                    Body=buffer.getvalue(),
                    ContentType='application/octet-stream'
                )
                
                logger.info(f"Uploaded to s3://{S3_CONFIG['bucket']}/{s3_key}")
                return
                
            except ClientError as e:
                if attempt < retries - 1:
                    logger.warning(f"Upload failed (attempt {attempt + 1}/{retries}): {e}")
                    continue
                else:
                    logger.error(f"Upload failed after {retries} attempts: {e}")
                    raise
    
    def export_all_tables(self, mode: str = 'incremental') -> bool:
        """
        Export all configured tables
        
        Args:
            mode: 'incremental' or 'full' export
            
        Returns:
            True if all exports succeeded
        """
        results = []
        
        for table in TABLES_TO_EXPORT:
            success = self.export_table(table, mode)
            results.append(success)
        
        all_success = all(results)
        
        if all_success:
            logger.info("All tables exported successfully")
        else:
            logger.error("Some tables failed to export")
        
        return all_success


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Export PostgreSQL to S3 for Athena')
    parser.add_argument(
        '--date',
        type=str,
        help='Export date in YYYY-MM-DD format (default: yesterday)'
    )
    parser.add_argument(
        '--mode',
        choices=['incremental', 'full'],
        default='incremental',
        help='Export mode: incremental (default) or full'
    )
    parser.add_argument(
        '--table',
        type=str,
        help='Specific table to export (default: all tables)'
    )
    
    args = parser.parse_args()
    
    # Parse date if provided
    export_date = None
    if args.date:
        try:
            export_date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            logger.error(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
            sys.exit(1)
    
    # Create exporter
    exporter = PostgresToS3Exporter(export_date)
    
    # Export tables
    if args.table:
        success = exporter.export_table(args.table, args.mode)
    else:
        success = exporter.export_all_tables(args.mode)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
