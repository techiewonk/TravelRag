#!/usr/bin/env python3
"""
Test script for ChromaDB travel vector database.

This script tests the ChromaDB implementation and travel tools.
"""

import os
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from typing import Any, Dict, List, Optional

# Import directly to avoid dependency issues
import chromadb
from chromadb.config import Settings


def get_chroma_client():
    """Get ChromaDB client with proper configuration."""
    try:
        client = chromadb.PersistentClient(
            path="./travel_chromadb",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=False
            )
        )
        return client
    except Exception as e:
        print(f"Error creating ChromaDB client: {e}")
        return None

def get_travel_collection():
    """Get the travel destinations ChromaDB collection."""
    try:
        client = get_chroma_client()
        if not client:
            return None
        
        # Try to get existing collection
        try:
            collection = client.get_collection("travel_destinations")
            return collection
        except Exception:
            print("Collection not found")
            return None
    except Exception as e:
        print(f"Error accessing travel collection: {e}")
        return None

def _parse_string_to_list(string_value: str) -> List[str]:
    """Parse comma-separated string back to list."""
    if not string_value:
        return []
    return [item.strip() for item in string_value.split(',') if item.strip()]

def search_destinations_chroma(query: str, n_results: int = 5) -> Dict[str, Any]:
    """Search for travel destinations using ChromaDB vector similarity search."""
    try:
        collection = get_travel_collection()
        if not collection:
            return {
                "success": False,
                "message": "Travel vector database not available. Please run the setup script first.",
                "destinations": []
            }
        
        # Check if collection is empty
        count = collection.count()
        if count == 0:
            return {
                "success": False,
                "message": "No destinations found in database. Please run the setup script to populate the database.",
                "destinations": []
            }
        
        # Perform vector search
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )
        
        destinations = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Convert distance to similarity score (lower distance = higher similarity)
            similarity_score = 1.0 - distance
            
            # Parse string fields back to lists
            famous_for = _parse_string_to_list(metadata.get('famous_for', ''))
            unique_offerings = _parse_string_to_list(metadata.get('unique_offerings', ''))
            
            destination = {
                "destination": metadata.get('destination', 'Unknown'),
                "description": metadata.get('description', ''),
                "famous_for": famous_for,
                "unique_offerings": unique_offerings,
                "region": metadata.get('region', ''),
                "country": metadata.get('country', ''),
                "other_characteristics": metadata.get('other_characteristics', ''),
                "best_time_to_travel": metadata.get('best_time_to_travel', ''),
                "similarity_score": similarity_score
            }
            destinations.append(destination)
        
        return {
            "success": True,
            "message": f"Found {len(destinations)} destinations matching '{query}'",
            "destinations": destinations,
            "query": query,
            "total_in_db": count
        }
        
    except Exception as e:
        print(f"Error searching destinations: {e}")
        return {
            "success": False,
            "message": f"Error searching destinations: {str(e)}",
            "destinations": []
        }

def get_destination_by_name_chroma(destination_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific destination by name."""
    try:
        collection = get_travel_collection()
        if not collection:
            return {
                "success": False,
                "message": "Travel vector database not available. Please run the setup script first.",
                "destination": None
            }
        
        # Check if collection is empty
        count = collection.count()
        if count == 0:
            return {
                "success": False,
                "message": "No destinations found in database. Please run the setup script to populate the database.",
                "destination": None
            }
        
        # Search for exact destination name
        results = collection.query(
            query_texts=[destination_name],
            n_results=10
        )
        
        # Find the best match
        best_match = None
        best_score = 0
        
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            similarity_score = 1.0 - distance
            dest_name = metadata.get('destination', '').lower()
            
            # Check for exact or close match
            if (dest_name == destination_name.lower() or 
                destination_name.lower() in dest_name or 
                dest_name in destination_name.lower()):
                if similarity_score > best_score:
                    best_score = similarity_score
                    best_match = {
                        "destination": metadata.get('destination', ''),
                        "description": metadata.get('description', ''),
                        "famous_for": _parse_string_to_list(metadata.get('famous_for', '')),
                        "unique_offerings": _parse_string_to_list(metadata.get('unique_offerings', '')),
                        "region": metadata.get('region', ''),
                        "country": metadata.get('country', ''),
                        "other_characteristics": metadata.get('other_characteristics', ''),
                        "best_time_to_travel": metadata.get('best_time_to_travel', ''),
                        "similarity_score": similarity_score
                    }
        
        if best_match:
            return {
                "success": True,
                "message": f"Found destination: {best_match['destination']}",
                "destination": best_match
            }
        else:
            return {
                "success": False,
                "message": f"Destination '{destination_name}' not found in database",
                "destination": None
            }
            
    except Exception as e:
        print(f"Error getting destination by name: {e}")
        return {
            "success": False,
            "message": f"Error getting destination: {str(e)}",
            "destination": None
        }

def search_destinations_by_criteria_chroma(
    country: Optional[str] = None,
    region: Optional[str] = None,
    activity_type: Optional[str] = None,
    best_time: Optional[str] = None,
    n_results: int = 10
) -> Dict[str, Any]:
    """Search destinations by specific criteria using ChromaDB."""
    try:
        collection = get_travel_collection()
        if not collection:
            return {
                "success": False,
                "message": "Travel vector database not available. Please run the setup script first.",
                "destinations": []
            }
        
        # Check if collection is empty
        count = collection.count()
        if count == 0:
            return {
                "success": False,
                "message": "No destinations found in database. Please run the setup script to populate the database.",
                "destinations": []
            }
        
        # Build search query based on criteria
        query_parts = []
        if country:
            query_parts.append(f"country {country}")
        if region:
            query_parts.append(f"region {region}")
        if activity_type:
            query_parts.append(f"{activity_type} activities")
        if best_time:
            query_parts.append(f"best time {best_time}")
        
        if not query_parts:
            query = "travel destinations"
        else:
            query = " ".join(query_parts)
        
        # Perform search
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, count)
        )
        
        destinations = []
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            # Apply filters
            if country and country.lower() not in metadata.get('country', '').lower():
                continue
            if region and region.lower() not in metadata.get('region', '').lower():
                continue
            
            similarity_score = 1.0 - distance
            destination = {
                "destination": metadata.get('destination', ''),
                "description": metadata.get('description', ''),
                "famous_for": _parse_string_to_list(metadata.get('famous_for', '')),
                "unique_offerings": _parse_string_to_list(metadata.get('unique_offerings', '')),
                "region": metadata.get('region', ''),
                "country": metadata.get('country', ''),
                "other_characteristics": metadata.get('other_characteristics', ''),
                "best_time_to_travel": metadata.get('best_time_to_travel', ''),
                "similarity_score": similarity_score
            }
            destinations.append(destination)
        
        return {
            "success": True,
            "message": f"Found {len(destinations)} destinations matching criteria",
            "destinations": destinations,
            "search_criteria": {
                "country": country,
                "region": region,
                "activity_type": activity_type,
                "best_time": best_time
            },
            "total_in_db": count
        }
        
    except Exception as e:
        print(f"Error searching destinations by criteria: {e}")
        return {
            "success": False,
            "message": f"Error searching destinations: {str(e)}",
            "destinations": []
        }

def get_database_stats_chroma() -> Dict[str, Any]:
    """Get statistics about the ChromaDB travel database."""
    try:
        collection = get_travel_collection()
        if not collection:
            return {
                "success": False,
                "message": "Travel vector database not available. Please run the setup script first.",
                "stats": None
            }
        
        count = collection.count()
        
        # Get sample of destinations for region/country stats
        if count > 0:
            sample_results = collection.query(
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
            
            stats = {
                "total_destinations": count,
                "unique_countries": len(countries),
                "unique_regions": len(regions),
                "sample_countries": sorted(list(countries))[:10],
                "sample_regions": sorted(list(regions))[:10]
            }
        else:
            stats = {
                "total_destinations": 0,
                "unique_countries": 0,
                "unique_regions": 0,
                "sample_countries": [],
                "sample_regions": []
            }
        
        return {
            "success": True,
            "message": f"Database contains {count} destinations",
            "stats": stats
        }
        
    except Exception as e:
        print(f"Error getting database stats: {e}")
        return {
            "success": False,
            "message": f"Error getting database stats: {str(e)}",
            "stats": None
        }


def test_database_stats():
    """Test database statistics."""
    print("Testing database statistics...")
    result = get_database_stats_chroma()
    
    if result["success"]:
        stats = result["stats"]
        print(f"SUCCESS: Database stats retrieved successfully:")
        print(f"  - Total destinations: {stats['total_destinations']}")
        print(f"  - Unique countries: {stats['unique_countries']}")
        print(f"  - Unique regions: {stats['unique_regions']}")
        print(f"  - Sample countries: {', '.join(stats['sample_countries'][:5])}")
        print(f"  - Sample regions: {', '.join(stats['sample_regions'][:5])}")
        return True
    else:
        print(f"ERROR: Failed to get database stats: {result['message']}")
        return False


def test_semantic_search():
    """Test semantic search functionality."""
    print("\nTesting semantic search...")
    
    test_queries = [
        "beach destinations",
        "cultural cities in Europe",
        "adventure travel destinations",
        "romantic getaways",
        "mountain hiking"
    ]
    
    all_passed = True
    
    for query in test_queries:
        print(f"\n  Testing query: '{query}'")
        result = search_destinations_chroma(query, n_results=3)
        
        if result["success"]:
            destinations = result["destinations"]
            print(f"  SUCCESS: Found {len(destinations)} destinations")
            
            if destinations:
                top_dest = destinations[0]
                print(f"    Top result: {top_dest['destination']} in {top_dest['country']} (score: {top_dest['similarity_score']:.3f})")
            else:
                print("    No destinations found")
        else:
            print(f"  ERROR: Search failed: {result['message']}")
            all_passed = False
    
    return all_passed


def test_destination_lookup():
    """Test destination lookup by name."""
    print("\nTesting destination lookup by name...")
    
    # First get some destinations to test with
    search_result = search_destinations_chroma("popular destinations", n_results=5)
    
    if not search_result["success"] or not search_result["destinations"]:
        print("ERROR: Cannot test destination lookup - no destinations available")
        return False
    
    # Test with the first few destinations
    test_destinations = [dest["destination"] for dest in search_result["destinations"][:3]]
    all_passed = True
    
    for dest_name in test_destinations:
        print(f"\n  Testing lookup: '{dest_name}'")
        result = get_destination_by_name_chroma(dest_name)
        
        if result["success"]:
            dest = result["destination"]
            print(f"  SUCCESS: Found: {dest['destination']} in {dest['country']}")
            print(f"    Description: {dest['description'][:100]}...")
            print(f"    Famous for: {', '.join(dest['famous_for'][:3])}")
        else:
            print(f"  ERROR: Lookup failed: {result['message']}")
            all_passed = False
    
    return all_passed


def test_criteria_search():
    """Test search by criteria."""
    print("\nTesting search by criteria...")
    
    test_criteria = [
        {"country": "France", "n_results": 3},
        {"region": "Europe", "n_results": 3},
        {"activity_type": "beach", "n_results": 3},
        {"country": "Japan", "activity_type": "cultural", "n_results": 3}
    ]
    
    all_passed = True
    
    for criteria in test_criteria:
        print(f"\n  Testing criteria: {criteria}")
        result = search_destinations_by_criteria_chroma(**criteria)
        
        if result["success"]:
            destinations = result["destinations"]
            print(f"  SUCCESS: Found {len(destinations)} destinations")
            
            if destinations:
                for dest in destinations[:2]:  # Show first 2 results
                    print(f"    - {dest['destination']} in {dest['country']} (score: {dest['similarity_score']:.3f})")
            else:
                print("    No destinations found matching criteria")
        else:
            print(f"  ERROR: Criteria search failed: {result['message']}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("ChromaDB Travel Vector Database Test Suite")
    print("=" * 50)
    
    # Check if database exists
    db_path = "./travel_chromadb"
    if not os.path.exists(db_path):
        print(f"ERROR: ChromaDB not found at {db_path}")
        print("Please run 'python scripts/create_chromadb_vector_db.py' first to create the database.")
        return False
    
    print(f"SUCCESS: Found ChromaDB at {db_path}")
    
    # Run tests
    tests = [
        ("Database Statistics", test_database_stats),
        ("Semantic Search", test_semantic_search),
        ("Destination Lookup", test_destination_lookup),
        ("Criteria Search", test_criteria_search)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR: Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! ChromaDB is working correctly.")
        return True
    else:
        print("Some tests failed. Please check the database setup.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)