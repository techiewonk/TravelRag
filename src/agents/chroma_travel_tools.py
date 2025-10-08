"""
Clean ChromaDB travel tools for destination search and management.
"""

import logging
import os
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from langchain_core.tools import tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DestinationSearchResult(BaseModel):
    """Model for destination search results."""
    destination: str
    description: str
    famous_for: List[str]
    unique_offerings: List[str]
    region: str
    country: str
    other_characteristics: str
    best_time_to_travel: str
    similarity_score: float


def get_chroma_client():
    """Get ChromaDB client with proper configuration."""
    try:
        # Use Docker path if running in container, otherwise use local path
        db_path = "/app/travel_chromadb" if os.path.exists("/app") else "./travel_chromadb"
        
        client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=False
            )
        )
        return client
    except Exception as e:
        logger.error(f"Error creating ChromaDB client: {e}")
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
            # Collection doesn't exist, create it
            collection = client.create_collection(
                name="travel_destinations",
                metadata={"description": "Travel destinations with embeddings"}
            )
            return collection
    except Exception as e:
        logger.error(f"Error accessing travel collection: {e}")
        return None


def _parse_string_to_list(string_value: str) -> List[str]:
    """Parse comma-separated string back to list."""
    if not string_value:
        return []
    return [item.strip() for item in string_value.split(',') if item.strip()]


@tool
def search_destinations_chroma(query: str, n_results: int = 5) -> Dict[str, Any]:
    """
    Search for travel destinations using ChromaDB vector similarity search.
    
    Args:
        query: Search query for destinations (e.g., "beach destinations", "cultural cities")
        n_results: Number of results to return (default: 5)
        
    Returns:
        Dictionary containing matching destinations with similarity scores
    """
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
            
            destination = DestinationSearchResult(
                destination=metadata.get('destination', 'Unknown'),
                description=metadata.get('description', ''),
                famous_for=famous_for,
                unique_offerings=unique_offerings,
                region=metadata.get('region', ''),
                country=metadata.get('country', ''),
                other_characteristics=metadata.get('other_characteristics', ''),
                best_time_to_travel=metadata.get('best_time_to_travel', ''),
                similarity_score=similarity_score
            )
            destinations.append(destination.model_dump())
        
        return {
            "success": True,
            "message": f"Found {len(destinations)} destinations matching '{query}'",
            "destinations": destinations,
            "query": query,
            "total_in_db": count
        }
        
    except Exception as e:
        logger.error(f"Error searching destinations: {e}")
        return {
            "success": False,
            "message": f"Error searching destinations: {str(e)}",
            "destinations": []
        }


@tool
def get_destination_by_name_chroma(destination_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific destination by name.
    
    Args:
        destination_name: Name of the destination to search for
        
    Returns:
        Dictionary containing detailed destination information
    """
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
        logger.error(f"Error getting destination by name: {e}")
        return {
            "success": False,
            "message": f"Error getting destination: {str(e)}",
            "destination": None
        }


@tool
def search_destinations_by_criteria_chroma(
    country: Optional[str] = None,
    region: Optional[str] = None,
    activity_type: Optional[str] = None,
    best_time: Optional[str] = None,
    n_results: int = 10
) -> Dict[str, Any]:
    """
    Search destinations by specific criteria using ChromaDB.
    
    Args:
        country: Filter by country
        region: Filter by region
        activity_type: Filter by activity type (e.g., "beach", "cultural", "adventure")
        best_time: Filter by best travel time
        n_results: Number of results to return
        
    Returns:
        Dictionary containing matching destinations
    """
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
        logger.error(f"Error searching destinations by criteria: {e}")
        return {
            "success": False,
            "message": f"Error searching destinations: {str(e)}",
            "destinations": []
        }


@tool
def get_database_stats_chroma() -> Dict[str, Any]:
    """
    Get statistics about the ChromaDB travel database.
    
    Returns:
        Dictionary containing database statistics
    """
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
        logger.error(f"Error getting database stats: {e}")
        return {
            "success": False,
            "message": f"Error getting database stats: {str(e)}",
            "stats": None
        }
