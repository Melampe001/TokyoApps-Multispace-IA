#!/usr/bin/env python3
"""
Dependency Agent - Validates pubspec.yaml dependencies
Only allows specific whitelisted dependencies.
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Set

# ALLOWED DEPENDENCIES - This is the whitelist
ALLOWED_DEPENDENCIES = {
    'flutter_riverpod',
    'shared_preferences',
    'path_provider',
}

# Always allowed SDK dependencies
ALLOWED_SDK_DEPENDENCIES = {
    'flutter',
}

def load_pubspec(file_path: str) -> Dict:
    """Load and parse pubspec.yaml file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: pubspec.yaml not found at {file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Invalid YAML in pubspec.yaml: {e}")
        sys.exit(1)

def check_dependencies(pubspec_data: Dict) -> tuple[bool, List[str]]:
    """
    Check if all dependencies are allowed.
    
    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    dependencies = pubspec_data.get('dependencies', {})
    
    if not dependencies:
        print("⚠️  WARNING: No dependencies found in pubspec.yaml")
        return True, []
    
    for dep_name, dep_config in dependencies.items():
        # Skip SDK dependencies (e.g., flutter: sdk: flutter)
        if isinstance(dep_config, dict) and dep_config.get('sdk'):
            if dep_name not in ALLOWED_SDK_DEPENDENCIES:
                violations.append(f"SDK dependency '{dep_name}' is not allowed")
            continue
        
        # Check if dependency is in whitelist
        if dep_name not in ALLOWED_DEPENDENCIES:
            violations.append(f"Dependency '{dep_name}' is not in the allowed list")
    
    return len(violations) == 0, violations

def print_report(is_valid: bool, violations: List[str], pubspec_data: Dict):
    """Print a formatted report of the dependency check."""
    print("\n" + "="*70)
    print("🔒 DEPENDENCY AGENT - Security Check Report")
    print("="*70)
    
    dependencies = pubspec_data.get('dependencies', {})
    dep_count = len([d for d in dependencies.keys() 
                     if not (isinstance(dependencies[d], dict) and dependencies[d].get('sdk'))])
    
    print(f"\n📦 Package: {pubspec_data.get('name', 'unknown')}")
    print(f"📊 Total dependencies found: {dep_count}")
    print(f"\n✅ Allowed dependencies:")
    for dep in sorted(ALLOWED_DEPENDENCIES):
        print(f"   - {dep}")
    
    if is_valid:
        print(f"\n✅ PASS - All dependencies are authorized")
        print("\n📋 Found dependencies:")
        for dep_name in dependencies.keys():
            if isinstance(dependencies[dep_name], dict) and dependencies[dep_name].get('sdk'):
                continue
            if dep_name in ALLOWED_DEPENDENCIES:
                print(f"   ✓ {dep_name}")
    else:
        print(f"\n❌ FAIL - Unauthorized dependencies detected!")
        print(f"\n🚨 Violations ({len(violations)}):")
        for i, violation in enumerate(violations, 1):
            print(f"   {i}. {violation}")
        
        print("\n📋 Current dependencies:")
        for dep_name, dep_config in dependencies.items():
            if isinstance(dep_config, dict) and dep_config.get('sdk'):
                print(f"   - {dep_name} (SDK)")
            elif dep_name in ALLOWED_DEPENDENCIES:
                print(f"   ✓ {dep_name} (allowed)")
            else:
                print(f"   ✗ {dep_name} (BLOCKED)")
    
    print("\n" + "="*70)

def main():
    """Main entry point."""
    # Find pubspec.yaml
    pubspec_path = Path('pubspec.yaml')
    
    if not pubspec_path.exists():
        # Try alternative locations
        alt_paths = [
            Path('.') / 'pubspec.yaml',
            Path('app') / 'pubspec.yaml',
            Path('flutter') / 'pubspec.yaml',
        ]
        
        for alt_path in alt_paths:
            if alt_path.exists():
                pubspec_path = alt_path
                break
        else:
            print("❌ ERROR: pubspec.yaml not found in any expected location")
            sys.exit(1)
    
    print(f"📂 Checking: {pubspec_path}")
    
    # Load and validate
    pubspec_data = load_pubspec(str(pubspec_path))
    is_valid, violations = check_dependencies(pubspec_data)
    
    # Print report
    print_report(is_valid, violations, pubspec_data)
    
    # Exit with appropriate code
    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
