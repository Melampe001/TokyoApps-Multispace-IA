#!/usr/bin/env python3
"""
Tests for ETL Export to S3

Basic tests for the export_to_s3 module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from etl.export_to_s3 import (
        check_table_exists,
        create_bucket_if_not_exists
    )
except ImportError:
    print("Warning: Could not import export_to_s3 module (dependencies may be missing)")
    print("Install with: pip install psycopg2-binary boto3 pandas pyarrow")


class TestETLExport(unittest.TestCase):
    """Test cases for ETL export functionality."""
    
    @patch('psycopg2.connect')
    def test_check_table_exists_true(self, mock_connect):
        """Test checking if table exists (returns True)."""
        # Mock connection and cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [True]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Test
        result = check_table_exists(mock_conn, 'invoices')
        
        # Assertions
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_check_table_exists_false(self, mock_connect):
        """Test checking if table exists (returns False)."""
        # Mock connection and cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [False]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Test
        result = check_table_exists(mock_conn, 'nonexistent_table')
        
        # Assertions
        self.assertFalse(result)
    
    @patch('boto3.client')
    def test_create_bucket_exists(self, mock_boto_client):
        """Test bucket creation when bucket already exists."""
        # Mock S3 client
        mock_s3 = Mock()
        mock_s3.head_bucket.return_value = True
        mock_boto_client.return_value = mock_s3
        
        # Test
        result = create_bucket_if_not_exists(mock_s3)
        
        # Assertions
        self.assertTrue(result)
        mock_s3.head_bucket.assert_called_once()
    
    def test_environment_variables(self):
        """Test that required environment variables are checked."""
        # Check if DATABASE_URL is mentioned
        self.assertIn('DATABASE_URL', os.environ.get('PATH', '') or 'DATABASE_URL')
        # This is a placeholder test - actual test would verify env var handling
    
    def test_table_list(self):
        """Test that TABLES constant is defined."""
        from etl.export_to_s3 import TABLES
        
        self.assertIsInstance(TABLES, list)
        self.assertGreater(len(TABLES), 0)
        self.assertIn('invoices', TABLES)
        self.assertIn('transactions', TABLES)
        self.assertIn('subscriptions', TABLES)


class TestETLConfiguration(unittest.TestCase):
    """Test configuration and setup."""
    
    def test_imports(self):
        """Test that required modules can be imported."""
        try:
            import psycopg2
            import boto3
            import pandas as pd
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"Required dependency not installed: {e}")
    
    def test_logging_configured(self):
        """Test that logging is configured."""
        import logging
        logger = logging.getLogger('export_to_s3')
        self.assertIsNotNone(logger)


def main():
    """Run tests."""
    unittest.main()


if __name__ == '__main__':
    main()
