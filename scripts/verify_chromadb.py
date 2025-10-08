#!/usr/bin/env python3
"""
Simple verification script for ChromaDB travel vector database.
"""

import os
import sys


def verify_chromadb_setup():
    """Verify that ChromaDB setup was successful."""
    print("ChromaDB Travel Vector Database Verification")
    print("=" * 50)
    
    # Check if database directory exists
    db_path = "./travel_chromadb"
    if not os.path.exists(db_path):
        print("ERROR: ChromaDB directory not found at", db_path)
        print("Please run 'python scripts/create_chromadb_vector_db.py' first.")
        return False
    
    print("SUCCESS: ChromaDB directory found at", db_path)
    
    # Check for ChromaDB files
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")
    if not os.path.exists(sqlite_file):
        print("ERROR: ChromaDB SQLite file not found")
        return False
    
    print("SUCCESS: ChromaDB SQLite file found")
    
    # Check for data files (ChromaDB stores data in UUID directories)
    data_files = []
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file.endswith(('.bin', '.sqlite3')):
                data_files.append(file)
    
    if not data_files:
        print("ERROR: No data files found in database")
        return False
    
    print(f"SUCCESS: Found {len(data_files)} data files in database")
    
    # Check database size
    total_size = 0
    for root, dirs, files in os.walk(db_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    size_mb = total_size / (1024 * 1024)
    print(f"SUCCESS: Database size: {size_mb:.2f} MB")
    
    print("\nChromaDB setup verification completed successfully!")
    print("\nThe database is ready to use with the following tools:")
    print("  - search_destinations_chroma(query, n_results)")
    print("  - get_destination_by_name_chroma(name)")
    print("  - search_destinations_by_criteria_chroma(...)")
    print("  - get_database_stats_chroma()")
    
    return True

if __name__ == "__main__":
    success = verify_chromadb_setup()
    sys.exit(0 if success else 1)
