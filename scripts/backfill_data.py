#!/usr/bin/env python3
"""
Backfill Historical Data
Loads historical data from PostgreSQL to S3 for a date range
"""

import sys
import logging
from datetime import datetime, timedelta
import argparse

# Add parent directory to path
sys.path.insert(0, 'python/etl')
from export_to_s3 import S3Exporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def backfill_data(start_date: datetime, end_date: datetime, table: str = None):
    """
    Backfill data for a date range

    Args:
        start_date: Start date for backfill
        end_date: End date for backfill
        table: Optional specific table to backfill
    """
    logger.info(f"Starting backfill from {start_date.date()} to {end_date.date()}")

    if end_date <= start_date:
        logger.error("End date must be after start date")
        return False

    days_to_process = (end_date - start_date).days
    logger.info(f"Processing {days_to_process} days of data")

    exporter = S3Exporter()

    current_date = start_date
    success_count = 0
    failure_count = 0

    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        logger.info(f"\nProcessing {current_date.date()}...")

        try:
            if table:
                # Backfill specific table
                result = exporter.export_table(
                    table_name=table,
                    date_column='created_at',
                    start_date=current_date,
                    end_date=next_date
                )

                if result['success']:
                    success_count += 1
                    logger.info(f"✓ Exported {result['total_rows']} rows from {table}")
                else:
                    failure_count += 1
                    logger.error(f"✗ Failed to export {table}: {result.get('errors', [])}")
            else:
                # Backfill all tables
                results = exporter.export_all_tables(current_date, next_date)

                day_success = sum(1 for r in results if r.get('success', False))
                day_failure = len(results) - day_success

                success_count += day_success
                failure_count += day_failure

                if day_failure == 0:
                    logger.info(f"✓ Completed all tables for {current_date.date()}")
                else:
                    logger.warning(f"⚠ {day_failure} table(s) failed for {current_date.date()}")

        except Exception as e:
            logger.error(f"✗ Error processing {current_date.date()}: {e}")
            failure_count += 1

        current_date = next_date

    # Summary
    logger.info("\n" + "="*80)
    logger.info("BACKFILL SUMMARY")
    logger.info("="*80)
    logger.info(f"Date range: {start_date.date()} to {end_date.date()}")
    logger.info(f"Days processed: {days_to_process}")
    logger.info(f"Successful exports: {success_count}")
    logger.info(f"Failed exports: {failure_count}")
    logger.info("="*80)

    return failure_count == 0


def main():
    """Main backfill entry point"""
    parser = argparse.ArgumentParser(
        description='Backfill historical data from PostgreSQL to S3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backfill last 7 days
  python backfill_data.py --start-date 2024-12-15 --end-date 2024-12-22

  # Backfill specific table for last 30 days
  python backfill_data.py --start-date 2024-11-22 --end-date 2024-12-22 --table workflows

  # Backfill full year
  python backfill_data.py --start-date 2024-01-01 --end-date 2024-12-31
        """
    )

    parser.add_argument(
        '--start-date',
        required=True,
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--end-date',
        required=True,
        help='End date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--table',
        help='Specific table to backfill (optional)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate backfill without actually exporting data'
    )

    args = parser.parse_args()

    # Parse dates
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError as e:
        logger.error(f"Invalid date format: {e}")
        logger.error("Use YYYY-MM-DD format (e.g., 2024-12-22)")
        sys.exit(1)

    # Validate date range
    if end_date <= start_date:
        logger.error("End date must be after start date")
        sys.exit(1)

    days_count = (end_date - start_date).days
    if days_count > 365:
        logger.warning(f"Large date range: {days_count} days")
        response = input("This will process a large amount of data. Continue? (y/n): ")
        if response.lower() != 'y':
            logger.info("Backfill cancelled")
            sys.exit(0)

    if args.dry_run:
        logger.info("DRY RUN MODE - No data will be exported")
        logger.info(f"Would backfill from {start_date.date()} to {end_date.date()}")
        logger.info(f"Days to process: {days_count}")
        if args.table:
            logger.info(f"Table: {args.table}")
        else:
            logger.info("Tables: all")
        sys.exit(0)

    # Run backfill
    success = backfill_data(start_date, end_date, args.table)

    if success:
        logger.info("✓ Backfill completed successfully")
        
        # Update Athena partitions
        logger.info("\nUpdating Athena partitions...")
        try:
            from athena_setup import AthenaSetup
            setup = AthenaSetup()
            
            tables = [args.table] if args.table else [
                'workflows', 'agent_tasks', 'agent_metrics',
                'agent_interactions', 'user_sessions'
            ]
            
            for table in tables:
                setup.repair_partitions(table)
            
            logger.info("✓ Partitions updated")
        except Exception as e:
            logger.warning(f"⚠ Failed to update partitions: {e}")
            logger.warning("You may need to run: python python/etl/athena_setup.py")
    else:
        logger.error("✗ Backfill completed with errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
