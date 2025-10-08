#!/usr/bin/env python3
"""
ChromaDB data seeding script for Docker containers.

This script checks if ChromaDB needs to be seeded and creates the database if it doesn't exist.
"""

import logging
import os
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_chromadb_exists():
    """Check if ChromaDB already exists and has data."""
    # Use correct path based on environment
    if os.path.exists("/app"):
        db_path = "/app/travel_chromadb"
    else:
        db_path = "./travel_chromadb"
    
    if not os.path.exists(db_path):
        logger.info("ChromaDB directory does not exist")
        return False
    
    # Check if SQLite file exists
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")
    if not os.path.exists(sqlite_file):
        logger.info("ChromaDB SQLite file does not exist")
        return False
    
    # Check if there are data files
    data_files = []
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if file.endswith(('.bin', '.sqlite3')):
                data_files.append(file)
    
    if not data_files:
        logger.info("No data files found in ChromaDB")
        return False
    
    logger.info(f"ChromaDB exists with {len(data_files)} data files")
    return True

def seed_chromadb():
    """Seed ChromaDB with travel destination data."""
    try:
        # Import the setup class
        sys.path.insert(0, str(Path(__file__).parent))
        from create_chromadb_vector_db import TravelChromaDBSetup
        
        logger.info("Starting ChromaDB seeding...")
        
        # Initialize setup with correct paths
        if os.path.exists("/app"):
            # Running in Docker
            db_path = "/app/travel_chromadb"
            csv_path = "/app/documents_rows.csv"
        else:
            # Running locally
            db_path = "./travel_chromadb"
            csv_path = "./documents_rows.csv"
        
        setup = TravelChromaDBSetup(
            db_path=db_path,
            csv_path=csv_path
        )
        
        # Check if CSV file exists
        if not os.path.exists(setup.csv_path):
            logger.error(f"CSV file not found at {setup.csv_path}")
            return False
        
        # Setup ChromaDB client
        logger.info("Setting up ChromaDB client...")
        if not setup.setup_client(reset_db=False):  # Don't reset existing data
            logger.error("Failed to setup ChromaDB client")
            return False
        
        # Check if database is already populated
        try:
            collection = setup.client.get_collection("travel_destinations")
            count = collection.count()
            if count > 0:
                logger.info(f"ChromaDB already contains {count} destinations. Skipping seeding.")
                return True
        except Exception:
            # Collection doesn't exist, we need to create it
            pass
        
        # Load CSV data
        logger.info("Loading CSV data...")
        destinations = setup.load_csv_data()
        if not destinations:
            logger.error("No destinations loaded from CSV")
            return False
        
        logger.info(f"Loaded {len(destinations)} destinations from CSV")
        
        # Populate database
        logger.info("Populating ChromaDB...")
        if not setup.populate_database(destinations):
            logger.error("Failed to populate database")
            return False
        
        logger.info("ChromaDB seeding completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during ChromaDB seeding: {e}")
        return False

def main():
    """Main function to check and seed ChromaDB if needed."""
    logger.info("ChromaDB Seeding Script")
    logger.info("=" * 40)
    
    # Check if ChromaDB already exists and has data
    if check_chromadb_exists():
        logger.info("ChromaDB already exists with data. No seeding needed.")
        return True
    
    # Seed ChromaDB
    logger.info("ChromaDB needs to be seeded...")
    success = seed_chromadb()
    
    if success:
        logger.info("ChromaDB seeding completed successfully!")
        return True
    else:
        logger.error("ChromaDB seeding failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
