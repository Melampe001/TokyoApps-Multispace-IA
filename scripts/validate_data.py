#!/usr/bin/env python3
"""
Data Validation Script
Validates that ETL exported data correctly to S3
"""

import sys
import logging
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import psycopg2
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, 'python/etl')
from config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataValidator:
    """Validates ETL data export"""

    def __init__(self):
        self.config = config
        self.s3_client = boto3.client(
            's3',
            region_name=self.config.aws_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )
        self.athena_client = boto3.client(
            'athena',
            region_name=self.config.aws_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )

    def check_s3_files(self, table_name: str, date: datetime) -> Dict[str, Any]:
        """Check if files exist in S3 for a given table and date"""
        prefix = f"{table_name}/year={date.year}/month={date.month:02d}/day={date.day:02d}/"

        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.config.s3_data_lake_bucket,
                Prefix=prefix
            )

            if 'Contents' not in response:
                return {
                    'exists': False,
                    'file_count': 0,
                    'total_size': 0
                }

            file_count = len(response['Contents'])
            total_size = sum(obj['Size'] for obj in response['Contents'])

            return {
                'exists': True,
                'file_count': file_count,
                'total_size': total_size,
                'prefix': prefix
            }

        except Exception as e:
            logger.error(f"Error checking S3 files for {table_name}: {e}")
            return {
                'exists': False,
                'error': str(e)
            }

    def count_db_rows(self, table_name: str, date: datetime) -> int:
        """Count rows in PostgreSQL for a given date"""
        try:
            conn = psycopg2.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                dbname=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password,
            )

            cursor = conn.cursor()
            
            # Determine date column based on table
            date_column = 'created_at'
            if table_name == 'agent_metrics':
                date_column = 'recorded_at'
            elif table_name == 'user_sessions':
                date_column = 'started_at'

            query = f"""
                SELECT COUNT(*)
                FROM {table_name}
                WHERE {date_column} >= %s::timestamp
                  AND {date_column} < %s::timestamp
            """

            next_date = date + timedelta(days=1)
            cursor.execute(query, (date, next_date))
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            return count

        except Exception as e:
            logger.error(f"Error counting DB rows for {table_name}: {e}")
            return -1

    def validate_partitions(self, table_name: str) -> Dict[str, Any]:
        """Validate Glue table partitions"""
        try:
            glue_client = boto3.client(
                'glue',
                region_name=self.config.aws_region,
                aws_access_key_id=self.config.aws_access_key_id,
                aws_secret_access_key=self.config.aws_secret_access_key,
            )

            response = glue_client.get_partitions(
                DatabaseName=self.config.athena_database,
                TableName=table_name,
                MaxResults=100
            )

            partitions = response.get('Partitions', [])

            return {
                'partition_count': len(partitions),
                'latest_partition': partitions[-1]['Values'] if partitions else None
            }

        except Exception as e:
            logger.error(f"Error validating partitions for {table_name}: {e}")
            return {
                'partition_count': 0,
                'error': str(e)
            }

    def validate_table(self, table_name: str, date: datetime) -> Dict[str, Any]:
        """Validate a table's data export"""
        logger.info(f"Validating {table_name} for {date.date()}")

        # Check S3 files
        s3_check = self.check_s3_files(table_name, date)

        # Count DB rows
        db_count = self.count_db_rows(table_name, date)

        # Validate partitions
        partition_check = self.validate_partitions(table_name)

        result = {
            'table': table_name,
            'date': date.date().isoformat(),
            's3_exists': s3_check['exists'],
            's3_file_count': s3_check.get('file_count', 0),
            's3_size_bytes': s3_check.get('total_size', 0),
            'db_row_count': db_count,
            'partition_count': partition_check['partition_count'],
            'valid': s3_check['exists'] and db_count >= 0
        }

        return result

    def run_validation(self, days_back: int = 1) -> List[Dict[str, Any]]:
        """Run validation for all tables"""
        tables = [
            'workflows',
            'agent_tasks',
            'agent_metrics',
            'agent_interactions',
            'user_sessions'
        ]

        results = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        for i in range(days_back):
            check_date = today - timedelta(days=i+1)

            for table in tables:
                result = self.validate_table(table, check_date)
                results.append(result)

        return results


def main():
    """Main validation entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Validate ETL data export')
    parser.add_argument(
        '--days',
        type=int,
        default=1,
        help='Number of days to validate (default: 1)'
    )

    args = parser.parse_args()

    validator = DataValidator()
    results = validator.run_validation(days_back=args.days)

    # Print results
    print("\n" + "="*80)
    print("ETL VALIDATION REPORT")
    print("="*80 + "\n")

    valid_count = 0
    invalid_count = 0

    for result in results:
        status = "✓" if result['valid'] else "✗"
        print(f"{status} {result['table']:20s} {result['date']:12s} | "
              f"S3: {result['s3_file_count']:2d} files "
              f"({result['s3_size_bytes']:,} bytes) | "
              f"DB: {result['db_row_count']:,} rows | "
              f"Partitions: {result['partition_count']}")

        if result['valid']:
            valid_count += 1
        else:
            invalid_count += 1

    print("\n" + "="*80)
    print(f"SUMMARY: {valid_count} passed, {invalid_count} failed")
    print("="*80 + "\n")

    # Exit with error if any validation failed
    if invalid_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
