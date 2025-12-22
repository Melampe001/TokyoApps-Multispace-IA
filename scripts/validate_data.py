#!/usr/bin/env python3
"""Validate data integrity in S3 and Athena"""

import os
import sys
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def validate_daily_export(date: datetime.date) -> bool:
    """Validates that data exists for the specified date"""
    s3 = boto3.client('s3')
    bucket = os.getenv('S3_DATA_LAKE_BUCKET', 'tokyo-ia-data-lake')
    
    tables = ['invoices', 'transactions', 'users', 'subscriptions']
    all_valid = True
    
    for table in tables:
        prefix = f"billing-data/{table}/year={date.year}/month={date.month:02d}/day={date.day:02d}/"
        
        try:
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
            
            if 'Contents' not in response:
                print(f"⚠️  No data found for {table} on {date}")
                all_valid = False
            else:
                file_count = len(response['Contents'])
                total_size = sum(obj['Size'] for obj in response['Contents'])
                print(f"✅ {table}: {file_count} files, {total_size / 1024 / 1024:.2f} MB")
        
        except ClientError as e:
            print(f"❌ Error checking {table}: {e}")
            all_valid = False
    
    return all_valid


def validate_athena_connectivity() -> bool:
    """Validates connectivity with Athena"""
    try:
        athena = boto3.client('athena')
        database = os.getenv('ATHENA_DATABASE', 'tokyo_ia_billing')
        workgroup = os.getenv('ATHENA_WORKGROUP', 'tokyo-ia-analytics')
        
        # Try to get workgroup info
        response = athena.get_work_group(WorkGroup=workgroup)
        print(f"✅ Athena workgroup '{workgroup}' is accessible")
        
        return True
    
    except ClientError as e:
        print(f"❌ Cannot access Athena: {e}")
        return False


def main():
    """Main entry point"""
    print("🔍 Validating data integrity...\n")
    
    # Get yesterday's date
    yesterday = datetime.now().date() - timedelta(days=1)
    
    # Validate Athena connectivity
    athena_ok = validate_athena_connectivity()
    print()
    
    # Validate daily export
    print(f"Checking data for {yesterday}...")
    export_ok = validate_daily_export(yesterday)
    
    print()
    if athena_ok and export_ok:
        print("✅ All validations passed!")
        sys.exit(0)
    else:
        print("❌ Some validations failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
