#!/usr/bin/env python3
"""
Unit tests for the dependency agent check_dependencies.py script
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the script directory to path - find repository root
def find_repo_root():
    """Find repository root by looking for .git directory"""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / '.git').exists():
            return parent
    return Path(__file__).parent.parent.parent

repo_root = find_repo_root()
script_dir = repo_root / '.github' / 'workflows' / 'bots' / 'scripts'
sys.path.insert(0, str(script_dir))

import check_dependencies

class TestDependencyChecker(unittest.TestCase):
    """Test cases for dependency validation"""
    
    def test_valid_dependencies(self):
        """Test that valid dependencies pass"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {
                'flutter': {'sdk': 'flutter'},
                'flutter_riverpod': '^2.4.10',
                'shared_preferences': '^2.2.2',
                'path_provider': '^2.1.2',
            }
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)
    
    def test_invalid_dependencies(self):
        """Test that invalid dependencies fail"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {
                'flutter': {'sdk': 'flutter'},
                'flutter_riverpod': '^2.4.10',
                'http': '^1.2.0',  # Not allowed
                'firebase_core': '^3.5.0',  # Not allowed
            }
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 2)
        self.assertIn("'http'", violations[0])
        self.assertIn("'firebase_core'", violations[1])
    
    def test_only_sdk_dependencies(self):
        """Test that SDK dependencies are allowed"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {
                'flutter': {'sdk': 'flutter'},
            }
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)
    
    def test_empty_dependencies(self):
        """Test handling of empty dependencies"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {}
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)
    
    def test_no_dependencies_key(self):
        """Test handling of missing dependencies key"""
        pubspec_data = {
            'name': 'test_app',
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)
    
    def test_mixed_valid_invalid(self):
        """Test mix of valid and invalid dependencies"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {
                'flutter': {'sdk': 'flutter'},
                'flutter_riverpod': '^2.4.10',  # Valid
                'shared_preferences': '^2.2.2',  # Valid
                'dio': '^5.0.0',  # Invalid
            }
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertFalse(is_valid)
        self.assertEqual(len(violations), 1)
        self.assertIn("'dio'", violations[0])
    
    def test_allowed_dependencies_set(self):
        """Test that the allowed dependencies set is correct"""
        expected_allowed = {'flutter_riverpod', 'shared_preferences', 'path_provider'}
        self.assertEqual(check_dependencies.ALLOWED_DEPENDENCIES, expected_allowed)
    
    def test_unauthorized_sdk_dependency(self):
        """Test that unauthorized SDK dependencies are blocked"""
        pubspec_data = {
            'name': 'test_app',
            'dependencies': {
                'flutter': {'sdk': 'flutter'},
                'sky_engine': {'sdk': 'flutter'},  # Not in allowed SDK deps
            }
        }
        
        is_valid, violations = check_dependencies.check_dependencies(pubspec_data)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(violations), 0)


class TestPubspecLoading(unittest.TestCase):
    """Test cases for pubspec.yaml loading"""
    
    def test_load_valid_yaml(self):
        """Test loading a valid pubspec.yaml"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
name: test_app
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.4.10
            """)
            temp_file = f.name
        
        try:
            pubspec_data = check_dependencies.load_pubspec(temp_file)
            self.assertIsNotNone(pubspec_data)
            self.assertEqual(pubspec_data['name'], 'test_app')
            self.assertIn('dependencies', pubspec_data)
        finally:
            os.unlink(temp_file)
    
    def test_load_invalid_yaml(self):
        """Test loading an invalid YAML file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
name: test_app
dependencies:
  flutter:
    sdk: flutter
  invalid: [unclosed list
            """)
            temp_file = f.name
        
        try:
            with self.assertRaises(SystemExit):
                check_dependencies.load_pubspec(temp_file)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
