#!/usr/bin/env python3
"""
Library Search - CLI tool for searching the library catalog
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime


class LibrarySearch:
    def __init__(self, index_path):
        self.index_path = Path(index_path)
        self.index_data = None
        self.load_index()

    def load_index(self):
        """Load the search index"""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.index_data = json.load(f)
            print(f"Loaded index with {self.index_data['total_files']} files")
        except FileNotFoundError:
            print(f"Error: Index file not found at {self.index_path}")
            print("Please run the library cataloger first.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in index file: {e}")
            sys.exit(1)

    def search(self, name=None, file_type=None, purpose=None, content=None, 
               author=None, since=None, extension=None):
        """Search for files based on criteria"""
        results = []
        
        for file_meta in self.index_data['files']:
            # Name search
            if name and name.lower() not in file_meta['file']['name'].lower():
                continue
            
            # Type search
            if file_type and file_meta['file']['type'] != file_type:
                continue
            
            # Purpose search
            if purpose and file_meta['classification']['purpose'] != purpose:
                continue
            
            # Content search (in description)
            if content and content.lower() not in file_meta['content']['description'].lower():
                continue
            
            # Author search
            if author and author.lower() not in file_meta['authorship']['author'].lower():
                continue
            
            # Date filter
            if since:
                try:
                    file_date = datetime.fromisoformat(file_meta['dates']['created'].replace('Z', '+00:00'))
                    since_date = datetime.fromisoformat(since)
                    if file_date < since_date:
                        continue
                except:
                    continue
            
            # Extension search
            if extension and file_meta['file']['extension'] != extension:
                continue
            
            results.append(file_meta)
        
        return results

    def display_results(self, results):
        """Display search results"""
        if not results:
            print("\n❌ No files found matching the criteria.")
            return
        
        print(f"\n✅ Found {len(results)} file(s):\n")
        
        for i, file_meta in enumerate(results, 1):
            print(f"{i}. {file_meta['file']['name']}")
            print(f"   Path: {file_meta['file']['path']}")
            print(f"   Type: {file_meta['file']['type']}")
            print(f"   Purpose: {file_meta['classification']['purpose']}")
            print(f"   Description: {file_meta['content']['description'][:100]}")
            print(f"   Author: {file_meta['authorship']['author']}")
            print(f"   Created: {file_meta['dates']['created']}")
            
            if file_meta['classification']['tags']:
                print(f"   Tags: {', '.join(file_meta['classification']['tags'])}")
            
            print()

    def list_categories(self):
        """List all available categories"""
        categories = set()
        types = set()
        purposes = set()
        
        for file_meta in self.index_data['files']:
            categories.add(file_meta['classification']['category'])
            types.add(file_meta['file']['type'])
            purposes.add(file_meta['classification']['purpose'])
        
        print("\n📚 Available Categories:")
        for cat in sorted(categories):
            print(f"  - {cat}")
        
        print("\n🗂️ Available Types:")
        for t in sorted(types):
            print(f"  - {t}")
        
        print("\n🎯 Available Purposes:")
        for p in sorted(purposes):
            print(f"  - {p}")


def main():
    parser = argparse.ArgumentParser(
        description='Search the Tokyo-IA library catalog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by name
  python library_search.py --name "jira"
  
  # Search by type
  python library_search.py --type "workflow"
  
  # Search by purpose
  python library_search.py --purpose "automation"
  
  # Full-text search in descriptions
  python library_search.py --content "github api"
  
  # Search by author
  python library_search.py --author "dev1"
  
  # Search by date
  python library_search.py --since "2025-12-01"
  
  # Combined search
  python library_search.py --type "script" --purpose "automation"
  
  # List all available categories
  python library_search.py --list
        """
    )
    
    parser.add_argument('--name', help='Search by file name')
    parser.add_argument('--type', help='Search by file type')
    parser.add_argument('--purpose', help='Search by purpose')
    parser.add_argument('--content', help='Full-text search in content/description')
    parser.add_argument('--author', help='Search by author')
    parser.add_argument('--since', help='Files created since date (YYYY-MM-DD)')
    parser.add_argument('--extension', help='Search by file extension')
    parser.add_argument('--list', action='store_true', help='List all available categories')
    parser.add_argument('--index', default='LIBRARY/SEARCH_INDEX.json', 
                       help='Path to search index (default: LIBRARY/SEARCH_INDEX.json)')
    
    args = parser.parse_args()
    
    # Default index path
    if not Path(args.index).is_absolute():
        args.index = Path.cwd() / args.index
    
    searcher = LibrarySearch(args.index)
    
    if args.list:
        searcher.list_categories()
        return
    
    # Perform search
    results = searcher.search(
        name=args.name,
        file_type=args.type,
        purpose=args.purpose,
        content=args.content,
        author=args.author,
        since=args.since,
        extension=args.extension
    )
    
    searcher.display_results(results)


if __name__ == '__main__':
    main()
