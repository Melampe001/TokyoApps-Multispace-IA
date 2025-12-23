"""
ETL Configuration Module
Centralized configuration and environment variable management
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ETLConfig:
    """Configuration class for ETL pipeline"""

    def __init__(self):
        self.validate_config()

    # PostgreSQL Configuration
    @property
    def db_host(self) -> str:
        return os.getenv("DB_HOST", "localhost")

    @property
    def db_port(self) -> int:
        return int(os.getenv("DB_PORT", "5432"))

    @property
    def db_name(self) -> str:
        return os.getenv("DB_NAME", "tokyo_ia")

    @property
    def db_user(self) -> str:
        return os.getenv("DB_USER", "postgres")

    @property
    def db_password(self) -> str:
        return os.getenv("DB_PASSWORD", "")

    @property
    def database_url(self) -> str:
        """Get PostgreSQL connection string"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # AWS Configuration
    @property
    def aws_region(self) -> str:
        return os.getenv("AWS_REGION", "us-east-1")

    @property
    def aws_access_key_id(self) -> Optional[str]:
        return os.getenv("AWS_ACCESS_KEY_ID")

    @property
    def aws_secret_access_key(self) -> Optional[str]:
        return os.getenv("AWS_SECRET_ACCESS_KEY")

    @property
    def s3_data_lake_bucket(self) -> str:
        return os.getenv("S3_DATA_LAKE_BUCKET", "tokyo-ia-data-lake-dev")

    @property
    def s3_athena_results_bucket(self) -> str:
        return os.getenv("S3_ATHENA_RESULTS_BUCKET", "tokyo-ia-athena-results-dev")

    # Athena Configuration
    @property
    def athena_database(self) -> str:
        return os.getenv("ATHENA_DATABASE", "tokyo_ia_billing_dev")

    @property
    def athena_workgroup(self) -> str:
        return os.getenv("ATHENA_WORKGROUP", "tokyo-ia-dev")

    # ETL Configuration
    @property
    def batch_size(self) -> int:
        return int(os.getenv("ETL_BATCH_SIZE", "10000"))

    @property
    def retention_days(self) -> int:
        return int(os.getenv("ETL_RETENTION_DAYS", "90"))

    @property
    def environment(self) -> str:
        return os.getenv("ENVIRONMENT", "dev")

    def validate_config(self) -> None:
        """Validate required configuration"""
        required_vars = [
            ("DB_HOST", self.db_host),
            ("DB_NAME", self.db_name),
            ("DB_USER", self.db_user),
            ("S3_DATA_LAKE_BUCKET", self.s3_data_lake_bucket),
            ("ATHENA_DATABASE", self.athena_database),
        ]

        missing = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing.append(var_name)

        if missing:
            raise ValueError(
                f"Missing required configuration variables: {', '.join(missing)}"
            )

    def __repr__(self) -> str:
        return (
            f"ETLConfig(environment={self.environment}, "
            f"db_host={self.db_host}, "
            f"s3_bucket={self.s3_data_lake_bucket}, "
            f"athena_db={self.athena_database})"
        )


# Global config instance
config = ETLConfig()
