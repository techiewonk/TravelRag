#!/usr/bin/env python3
"""
Test script to verify ChromaDB works in Docker environment.
"""

import os
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_chromadb_in_docker():
    """Test ChromaDB functionality in Docker environment."""
    print("Testing ChromaDB in Docker environment...")
    print("=" * 50)
    
    # Check if we're in Docker
    if os.path.exists("/app"):
        print("SUCCESS: Running in Docker container")
        db_path = "/app/travel_chromadb"
    else:
        print("INFO: Running locally")
        db_path = "./travel_chromadb"
    
    print(f"ChromaDB path: {db_path}")
    
    # Check if ChromaDB directory exists
    if not os.path.exists(db_path):
        print(f"ERROR: ChromaDB directory not found at {db_path}")
        return False
    
    print("SUCCESS: ChromaDB directory found")
    
    # Try to import and use ChromaDB tools
    try:
        from agents.chroma_travel_tools import get_database_stats_chroma
        
        print("SUCCESS: ChromaDB tools imported successfully")
        
        # Test database stats
        result = get_database_stats_chroma()
        
        if result["success"]:
            stats = result["stats"]
            print(f"SUCCESS: Database stats retrieved:")
            print(f"  - Total destinations: {stats['total_destinations']}")
            print(f"  - Unique countries: {stats['unique_countries']}")
            print(f"  - Unique regions: {stats['unique_regions']}")
            return True
        else:
            print(f"ERROR: Failed to get database stats: {result['message']}")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to import or use ChromaDB tools: {e}")
        return False

if __name__ == "__main__":
    success = test_chromadb_in_docker()
    if success:
        print("\nChromaDB Docker test completed successfully!")
    else:
        print("\nChromaDB Docker test failed!")
    sys.exit(0 if success else 1)
