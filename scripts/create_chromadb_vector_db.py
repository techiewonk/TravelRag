#!/usr/bin/env python3
"""
Create ChromaDB vector database for travel destinations.

This script loads travel destination data from CSV and creates a ChromaDB collection
with vector embeddings for semantic search capabilities.
"""

import csv
import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TravelChromaDBSetup:
    """Setup and manage ChromaDB for travel destinations."""
    
    def __init__(self, db_path: str = "./travel_chromadb", csv_path: str = "./documents_rows.csv"):
        self.db_path = db_path
        self.csv_path = csv_path
        self.client = None
        self.collection = None
    
    def setup_client(self, reset_db: bool = False) -> bool:
        """Initialize ChromaDB client and collection."""
        try:
            # Remove existing database if reset is requested
            if reset_db and os.path.exists(self.db_path):
                shutil.rmtree(self.db_path)
                logger.info(f"Removed existing database at {self.db_path}")
            
            # Create client
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection("travel_destinations")
                logger.info("Using existing travel_destinations collection")
            except Exception:
                self.collection = self.client.create_collection(
                    name="travel_destinations",
                    metadata={"description": "Travel destinations with embeddings"}
                )
                logger.info("Created new travel_destinations collection")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up ChromaDB client: {e}")
            return False
    
    def load_csv_data(self) -> List[Dict[str, Any]]:
        """Load and parse CSV data."""
        if not os.path.exists(self.csv_path):
            logger.error(f"CSV file not found: {self.csv_path}")
            return []
        
        destinations = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                # Detect delimiter
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(file, delimiter=delimiter)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Clean and process the row
                        destination = self._process_row(row)
                        if destination:
                            destinations.append(destination)
                    except Exception as e:
                        logger.warning(f"Error processing row {row_num}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return []
        
        logger.info(f"Loaded {len(destinations)} destinations from CSV")
        return destinations
    
    def _process_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Process a single CSV row into a destination dictionary."""
        try:
            # Check if this is the new format with content field
            if 'content' in row and row['content']:
                return self._process_content_row(row)
            
            # Original format processing
            destination = row.get('destination', '').strip()
            if not destination:
                return None
            
            description = row.get('description', '').strip()
            famous_for = self._parse_list_field(row.get('famous_for', ''))
            unique_offerings = self._parse_list_field(row.get('unique_offerings', ''))
            region = row.get('region', '').strip()
            country = row.get('country', '').strip()
            other_characteristics = row.get('other_characteristics', '').strip()
            best_time_to_travel = row.get('best_time_to_travel', '').strip()
            
            # Create comprehensive text description for embedding
            text_parts = [
                f"Destination: {destination}",
                f"Description: {description}",
                f"Country: {country}",
                f"Region: {region}"
            ]
            
            if famous_for:
                text_parts.append(f"Famous for: {', '.join(famous_for)}")
            
            if unique_offerings:
                text_parts.append(f"Unique offerings: {', '.join(unique_offerings)}")
            
            if other_characteristics:
                text_parts.append(f"Characteristics: {other_characteristics}")
            
            if best_time_to_travel:
                text_parts.append(f"Best time to travel: {best_time_to_travel}")
            
            document_text = " | ".join(text_parts)
            
            return {
                'destination': destination,
                'description': description,
                'famous_for': famous_for,
                'unique_offerings': unique_offerings,
                'region': region,
                'country': country,
                'other_characteristics': other_characteristics,
                'best_time_to_travel': best_time_to_travel,
                'document_text': document_text
            }
            
        except Exception as e:
            logger.warning(f"Error processing row: {e}")
            return None
    
    def _process_content_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Process a row with content field (new format)."""
        try:
            content = row.get('content', '').strip()
            if not content:
                return None
            
            # Parse the content field which contains structured data
            lines = content.split('\n')
            data = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    data[key] = value
            
            # Extract destination name from the content
            destination = data.get('destination', '').strip()
            if not destination:
                return None
            
            # Parse list fields
            famous_for = self._parse_list_field(data.get('famous_for', ''))
            unique_offerings = self._parse_list_field(data.get('unique_offerings', ''))
            
            # Create document text (use the original content)
            document_text = content
            
            return {
                'destination': destination,
                'description': data.get('description', ''),
                'famous_for': famous_for,
                'unique_offerings': unique_offerings,
                'region': data.get('region', ''),
                'country': data.get('country', ''),
                'other_characteristics': data.get('other_characteristics', ''),
                'best_time_to_travel': data.get('best_time_to_travel', ''),
                'document_text': document_text
            }
            
        except Exception as e:
            logger.warning(f"Error processing content row: {e}")
            return None
    
    def _parse_list_field(self, field_value: str) -> List[str]:
        """Parse comma-separated list field."""
        if not field_value:
            return []
        
        # Split by comma and clean each item
        items = [item.strip() for item in field_value.split(',')]
        return [item for item in items if item]
    
    def populate_database(self, destinations: List[Dict[str, Any]]) -> bool:
        """Populate ChromaDB with destination data."""
        if not self.collection:
            logger.error("Collection not initialized")
            return False
        
        if not destinations:
            logger.error("No destinations to add")
            return False
        
        try:
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            for i, dest in enumerate(destinations):
                dest_id = f"dest_{i+1}"
                ids.append(dest_id)
                documents.append(dest['document_text'])
                
                # Create metadata (exclude document_text and convert lists to strings)
                metadata = {}
                for k, v in dest.items():
                    if k != 'document_text':
                        if isinstance(v, list):
                            metadata[k] = ', '.join(v)  # Convert list to comma-separated string
                        else:
                            metadata[k] = v
                metadatas.append(metadata)
            
            # Add to collection in batches to avoid memory issues
            batch_size = 100
            total_added = 0
            
            for i in range(0, len(ids), batch_size):
                batch_ids = ids[i:i+batch_size]
                batch_docs = documents[i:i+batch_size]
                batch_metadata = metadatas[i:i+batch_size]
                
                self.collection.add(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metadata
                )
                
                total_added += len(batch_ids)
                logger.info(f"Added batch {i//batch_size + 1}: {len(batch_ids)} destinations")
            
            logger.info(f"Successfully added {total_added} destinations to ChromaDB")
            return True
            
        except Exception as e:
            logger.error(f"Error populating database: {e}")
            return False
    
    def test_database(self) -> bool:
        """Test the database with sample queries."""
        if not self.collection:
            logger.error("Collection not initialized")
            return False
        
        try:
            # Get collection count
            count = self.collection.count()
            logger.info(f"Database contains {count} destinations")
            
            if count == 0:
                logger.warning("Database is empty")
                return False
            
            # Test queries
            test_queries = [
                "beach destinations",
                "cultural cities in Europe",
                "adventure travel",
                "romantic getaways"
            ]
            
            for query in test_queries:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=3
                )
                
                logger.info(f"Query '{query}' returned {len(results['documents'][0])} results")
                
                # Show first result
                if results['documents'][0]:
                    first_result = results['metadatas'][0][0]
                    logger.info(f"  Top result: {first_result.get('destination', 'Unknown')} in {first_result.get('country', 'Unknown')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error testing database: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get information about the database."""
        if not self.collection:
            return {"error": "Collection not initialized"}
        
        try:
            count = self.collection.count()
            
            # Get sample destinations for statistics
            if count > 0:
                sample_results = self.collection.query(
                    query_texts=["travel destinations"],
                    n_results=min(100, count)
                )
                
                countries = set()
                regions = set()
                
                for metadata in sample_results['metadatas'][0]:
                    if metadata.get('country'):
                        countries.add(metadata['country'])
                    if metadata.get('region'):
                        regions.add(metadata['region'])
                
                return {
                    "total_destinations": count,
                    "unique_countries": len(countries),
                    "unique_regions": len(regions),
                    "sample_countries": sorted(list(countries))[:10],
                    "sample_regions": sorted(list(regions))[:10],
                    "database_path": self.db_path
                }
            else:
                return {
                    "total_destinations": 0,
                    "unique_countries": 0,
                    "unique_regions": 0,
                    "sample_countries": [],
                    "sample_regions": [],
                    "database_path": self.db_path
                }
                
        except Exception as e:
            return {"error": f"Error getting database info: {e}"}


def main():
    """Main function to set up ChromaDB."""
    print("ChromaDB Travel Vector Database Setup")
    print("=" * 50)
    
    # Initialize setup
    setup = TravelChromaDBSetup()
    
    # Check if CSV file exists
    if not os.path.exists(setup.csv_path):
        print(f"ERROR: CSV file not found at {setup.csv_path}")
        print("Please ensure the documents_rows.csv file exists in the project root.")
        return False
    
    # Setup ChromaDB client
    print("Setting up ChromaDB client...")
    if not setup.setup_client(reset_db=True):
        print("ERROR: Failed to setup ChromaDB client")
        return False
    print("SUCCESS: ChromaDB client initialized")
    
    # Load CSV data
    print("Loading CSV data...")
    destinations = setup.load_csv_data()
    if not destinations:
        print("ERROR: No destinations loaded from CSV")
        return False
    print(f"SUCCESS: Loaded {len(destinations)} destinations")
    
    # Populate database
    print("Populating ChromaDB...")
    if not setup.populate_database(destinations):
        print("ERROR: Failed to populate database")
        return False
    print("SUCCESS: Database populated successfully")
    
    # Test database
    print("Testing database...")
    if not setup.test_database():
        print("ERROR: Database test failed")
        return False
    print("SUCCESS: Database test passed")
    
    # Show database info
    print("\nDatabase Information:")
    info = setup.get_database_info()
    if "error" not in info:
        print(f"  - Total destinations: {info['total_destinations']}")
        print(f"  - Unique countries: {info['unique_countries']}")
        print(f"  - Unique regions: {info['unique_regions']}")
        print(f"  - Database path: {info['database_path']}")
        print(f"  - Sample countries: {', '.join(info['sample_countries'][:5])}")
        print(f"  - Sample regions: {', '.join(info['sample_regions'][:5])}")
    else:
        print(f"  ERROR: {info['error']}")
    
    print("\nChromaDB setup completed successfully!")
    print("\nYou can now use the travel tools:")
    print("  - search_destinations_chroma(query, n_results)")
    print("  - get_destination_by_name_chroma(name)")
    print("  - search_destinations_by_criteria_chroma(...)")
    print("  - get_database_stats_chroma()")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
