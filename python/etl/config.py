"""Configuration for ETL pipeline"""

import os
from typing import Dict, Any

# PostgreSQL Configuration
POSTGRES_CONFIG: Dict[str, Any] = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'tokyo_ia'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', '5432'))
}

# S3 Configuration
S3_CONFIG: Dict[str, str] = {
    'bucket': os.getenv('S3_DATA_LAKE_BUCKET', 'tokyo-ia-data-lake'),
    'region': os.getenv('AWS_REGION', 'us-east-1'),
    'prefix': 'billing-data'
}

# Athena Configuration
ATHENA_CONFIG: Dict[str, str] = {
    'database': os.getenv('ATHENA_DATABASE', 'tokyo_ia_billing'),
    'workgroup': os.getenv('ATHENA_WORKGROUP', 'tokyo-ia-analytics'),
    'output_location': os.getenv('ATHENA_OUTPUT_LOCATION', 's3://tokyo-ia-athena-results/')
}

# Tables to export
TABLES_TO_EXPORT = ['invoices', 'transactions', 'users', 'subscriptions']

# Partition configuration
PARTITION_COLUMNS = ['year', 'month', 'day']

# Parquet configuration
PARQUET_CONFIG: Dict[str, Any] = {
    'compression': 'snappy',
    'row_group_size': 100000
}
