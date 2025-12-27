#!/usr/bin/env python3
"""
ETL Pipeline: Export PostgreSQL to S3 Data Lake

Exports data from PostgreSQL to S3 in Parquet format with partitioning.
Tables exported: invoices, transactions, users, subscriptions
Partitioning: year/month/day
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
import logging

try:
    import psycopg2
    import boto3
    import pandas as pd
    from botocore.exceptions import ClientError
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install psycopg2-binary boto3 pandas pyarrow")
    sys.exit(1)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET = os.getenv('S3_DATA_LAKE_BUCKET', 'tokyo-ia-data-lake')

# Tables to export
TABLES = ['invoices', 'transactions', 'users', 'subscriptions']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_db_connection():
    """Create PostgreSQL database connection."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        logger.info("Database connection established")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def get_s3_client():
    """Create S3 client."""
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials not set")
    
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        logger.info("S3 client created")
        return client
    except Exception as e:
        logger.error(f"S3 client creation failed: {e}")
        raise


def check_table_exists(conn, table_name: str) -> bool:
    """Check if table exists in database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
        """, (table_name,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists
    except psycopg2.Error as e:
        logger.warning(f"Error checking table {table_name}: {e}")
        return False


def export_table_to_s3(conn, s3_client, table_name: str, date: datetime) -> bool:
    """Export a table to S3 as Parquet."""
    logger.info(f"Exporting table: {table_name}")
    
    try:
        # Check if table exists
        if not check_table_exists(conn, table_name):
            logger.warning(f"Table {table_name} does not exist, skipping")
            return False
        
        # Read data from PostgreSQL
        query = f"SELECT * FROM {table_name}"
        logger.info(f"Executing query: {query}")
        df = pd.read_sql(query, conn)
        
        if df.empty:
            logger.warning(f"Table {table_name} is empty, skipping")
            return False
        
        logger.info(f"Read {len(df)} rows from {table_name}")
        
        # Create partition path
        year = date.year
        month = date.month
        day = date.day
        
        s3_key = f"data/{table_name}/year={year}/month={month:02d}/day={day:02d}/data.parquet"
        logger.info(f"Writing to s3://{S3_BUCKET}/{s3_key}")
        
        # Convert DataFrame to Parquet in memory
        parquet_buffer = df.to_parquet(
            engine='pyarrow',
            compression='snappy',
            index=False
        )
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=parquet_buffer
        )
        
        logger.info(f"Successfully exported {table_name} to S3")
        return True
        
    except pd.io.sql.DatabaseError as e:
        logger.error(f"Database error exporting {table_name}: {e}")
        return False
    except ClientError as e:
        logger.error(f"S3 error exporting {table_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error exporting {table_name}: {e}")
        return False


def create_bucket_if_not_exists(s3_client) -> bool:
    """Create S3 bucket if it doesn't exist."""
    try:
        s3_client.head_bucket(Bucket=S3_BUCKET)
        logger.info(f"Bucket {S3_BUCKET} exists")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logger.info(f"Creating bucket {S3_BUCKET}")
            try:
                if AWS_REGION == 'us-east-1':
                    s3_client.create_bucket(Bucket=S3_BUCKET)
                else:
                    s3_client.create_bucket(
                        Bucket=S3_BUCKET,
                        CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
                    )
                logger.info(f"Bucket {S3_BUCKET} created")
                return True
            except ClientError as ce:
                logger.error(f"Failed to create bucket: {ce}")
                return False
        else:
            logger.error(f"Error checking bucket: {e}")
            return False


def export_to_s3():
    """Main export function."""
    logger.info("Starting ETL pipeline: PostgreSQL → S3")
    
    # Validate configuration
    if not DATABASE_URL:
        logger.error("DATABASE_URL not set")
        return False
    
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("AWS credentials not set")
        return False
    
    try:
        # Get current date for partitioning
        export_date = datetime.now()
        logger.info(f"Export date: {export_date.strftime('%Y-%m-%d')}")
        
        # Create connections
        conn = get_db_connection()
        s3_client = get_s3_client()
        
        # Create bucket if needed
        if not create_bucket_if_not_exists(s3_client):
            logger.error("Failed to create/access S3 bucket")
            return False
        
        # Export each table
        results = {}
        for table in TABLES:
            success = export_table_to_s3(conn, s3_client, table, export_date)
            results[table] = success
        
        # Close connection
        conn.close()
        logger.info("Database connection closed")
        
        # Summary
        successful = sum(1 for v in results.values() if v)
        total = len(results)
        logger.info(f"Export completed: {successful}/{total} tables successful")
        
        for table, success in results.items():
            status = "✓" if success else "✗"
            logger.info(f"  {status} {table}")
        
        return successful == total
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        return False


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("Tokyo-IA Data Lake ETL Pipeline")
    logger.info("=" * 60)
    
    success = export_to_s3()
    
    if success:
        logger.info("ETL pipeline completed successfully")
        return 0
    else:
        logger.error("ETL pipeline completed with errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
