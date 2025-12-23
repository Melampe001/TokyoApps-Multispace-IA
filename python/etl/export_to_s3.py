"""
PostgreSQL to S3 Exporter
Exports historical data from PostgreSQL to S3 in Parquet format
with partitioning by year/month/day
"""

import logging
import sys
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import psycopg2
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class S3Exporter:
    """Exports PostgreSQL data to S3 in Parquet format"""

    def __init__(self):
        self.config = config
        self.s3_client = boto3.client(
            "s3",
            region_name=self.config.aws_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )
        self.conn = None

    def connect_db(self) -> None:
        """Establish PostgreSQL connection"""
        try:
            self.conn = psycopg2.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                dbname=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password,
            )
            logger.info("Connected to PostgreSQL database")
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def close_db(self) -> None:
        """Close PostgreSQL connection"""
        if self.conn:
            self.conn.close()
            logger.info("Closed database connection")

    def fetch_data(
        self, table_name: str, date_column: str, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Fetch data from PostgreSQL table for a date range

        Args:
            table_name: Name of the table to export
            date_column: Column name containing the date
            start_date: Start date for data export
            end_date: End date for data export

        Returns:
            DataFrame with fetched data
        """
        # Validate table and column names against whitelist
        valid_tables = ['workflows', 'agent_tasks', 'agent_metrics', 'agent_interactions', 'user_sessions']
        valid_columns = ['created_at', 'recorded_at', 'started_at']
        
        if table_name not in valid_tables:
            raise ValueError(f"Invalid table name: {table_name}")
        if date_column not in valid_columns:
            raise ValueError(f"Invalid date column: {date_column}")
        
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE {date_column} >= %s AND {date_column} < %s
            ORDER BY {date_column}
        """

        try:
            logger.info(
                f"Fetching data from {table_name} between {start_date} and {end_date}"
            )
            df = pd.read_sql_query(query, self.conn, params=(start_date, end_date))
            logger.info(f"Fetched {len(df)} rows from {table_name}")
            return df
        except Exception as e:
            logger.error(f"Error fetching data from {table_name}: {e}")
            raise

    def upload_to_s3(
        self,
        df: pd.DataFrame,
        table_name: str,
        year: int,
        month: int,
        day: int,
    ) -> bool:
        """
        Upload DataFrame to S3 as Parquet file with partitioning

        Args:
            df: DataFrame to upload
            table_name: Name of the table
            year: Year partition
            month: Month partition
            day: Day partition

        Returns:
            True if upload successful, False otherwise
        """
        if df.empty:
            logger.info(f"No data to upload for {table_name} on {year}-{month:02d}-{day:02d}")
            return True

        # Create S3 key with partitioning
        s3_key = f"{table_name}/year={year}/month={month:02d}/day={day:02d}/data.parquet"

        try:
            # Convert DataFrame to Parquet in memory
            buffer = BytesIO()
            df.to_parquet(
                buffer,
                engine="pyarrow",
                compression="snappy",
                index=False,
            )
            buffer.seek(0)

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.config.s3_data_lake_bucket,
                Key=s3_key,
                Body=buffer.getvalue(),
                ContentType="application/octet-stream",
            )

            logger.info(
                f"Uploaded {len(df)} rows to s3://{self.config.s3_data_lake_bucket}/{s3_key}"
            )
            return True

        except ClientError as e:
            logger.error(f"Failed to upload to S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            return False

    def export_table(
        self,
        table_name: str,
        date_column: str = "created_at",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Export a table to S3 with daily partitioning

        Args:
            table_name: Name of the table to export
            date_column: Column containing the date
            start_date: Start date (defaults to yesterday)
            end_date: End date (defaults to today)

        Returns:
            Dictionary with export statistics
        """
        if start_date is None:
            start_date = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            ) - timedelta(days=1)

        if end_date is None:
            end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        logger.info(f"Starting export for {table_name} from {start_date} to {end_date}")

        stats = {
            "table_name": table_name,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_rows": 0,
            "files_uploaded": 0,
            "success": True,
            "errors": [],
        }

        try:
            self.connect_db()

            # Process each day
            current_date = start_date
            while current_date < end_date:
                next_date = current_date + timedelta(days=1)

                # Fetch data for the day
                df = self.fetch_data(table_name, date_column, current_date, next_date)

                if not df.empty:
                    # Upload to S3
                    success = self.upload_to_s3(
                        df,
                        table_name,
                        current_date.year,
                        current_date.month,
                        current_date.day,
                    )

                    if success:
                        stats["total_rows"] += len(df)
                        stats["files_uploaded"] += 1
                    else:
                        stats["errors"].append(
                            f"Failed to upload data for {current_date.date()}"
                        )
                        stats["success"] = False

                current_date = next_date

            logger.info(
                f"Export completed for {table_name}: "
                f"{stats['total_rows']} rows, {stats['files_uploaded']} files"
            )

        except Exception as e:
            logger.error(f"Error during export: {e}")
            stats["success"] = False
            stats["errors"].append(str(e))
        finally:
            self.close_db()

        return stats

    def export_all_tables(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Export all relevant tables to S3

        Args:
            start_date: Start date for export
            end_date: End date for export

        Returns:
            List of export statistics for each table
        """
        tables = [
            ("workflows", "created_at"),
            ("agent_tasks", "created_at"),
            ("agent_metrics", "recorded_at"),
            ("agent_interactions", "created_at"),
            ("user_sessions", "started_at"),
        ]

        results = []
        for table_name, date_column in tables:
            try:
                stats = self.export_table(table_name, date_column, start_date, end_date)
                results.append(stats)
            except Exception as e:
                logger.error(f"Failed to export {table_name}: {e}")
                results.append(
                    {
                        "table_name": table_name,
                        "success": False,
                        "errors": [str(e)],
                    }
                )

        return results


def main():
    """Main entry point for ETL script"""
    import argparse

    parser = argparse.ArgumentParser(description="Export PostgreSQL data to S3")
    parser.add_argument(
        "--table",
        help="Specific table to export (default: all tables)",
    )
    parser.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD, default: yesterday)",
    )
    parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
    )

    args = parser.parse_args()

    # Parse dates
    start_date = None
    end_date = None

    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")

    if args.end_date:
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Create exporter
    exporter = S3Exporter()

    # Export data
    if args.table:
        results = [exporter.export_table(args.table, "created_at", start_date, end_date)]
    else:
        results = exporter.export_all_tables(start_date, end_date)

    # Print summary
    print("\n=== Export Summary ===")
    total_rows = sum(r.get("total_rows", 0) for r in results)
    total_files = sum(r.get("files_uploaded", 0) for r in results)
    success_count = sum(1 for r in results if r.get("success", False))

    print(f"Tables processed: {len(results)}")
    print(f"Successful exports: {success_count}/{len(results)}")
    print(f"Total rows exported: {total_rows}")
    print(f"Total files uploaded: {total_files}")

    # Exit with error if any exports failed
    if success_count < len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
