"""
Amadeus travel tools for flight and hotel search using the Amadeus API.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_core.tools import tool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Set up Amadeus credentials
os.environ["AMADEUS_CLIENT_ID"] = os.getenv("AMADEUS_CLIENT_ID", "CLIENT_ID")
os.environ["AMADEUS_CLIENT_SECRET"] = os.getenv("AMADEUS_CLIENT_SECRET", "CLIENT_SECRET")

# Initialize Amadeus toolkit
try:
    toolkit = AmadeusToolkit()
    amadeus_tools = toolkit.get_tools()
    logger.info(f"Amadeus toolkit initialized with {len(amadeus_tools)} tools")
except Exception as e:
    logger.error(f"Failed to initialize Amadeus toolkit: {e}")
    amadeus_tools = []


class FlightSearchRequest(BaseModel):
    """Model for flight search requests."""
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int = 1
    children: int = 0
    infants: int = 0
    travel_class: str = "ECONOMY"


class HotelSearchRequest(BaseModel):
    """Model for hotel search requests."""
    city_code: str
    check_in: str
    check_out: str
    adults: int = 2
    rooms: int = 1
    currency: str = "USD"


@tool
def search_flights_amadeus(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
    travel_class: str = "ECONOMY"
) -> Dict[str, Any]:
    """
    Search for flights using Amadeus API.
    
    Args:
        origin: Origin airport/city code (e.g., "NYC", "LON")
        destination: Destination airport/city code (e.g., "PAR", "TOK")
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (optional for one-way)
        adults: Number of adult passengers
        children: Number of child passengers
        infants: Number of infant passengers
        travel_class: Travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)
        
    Returns:
        Dictionary containing flight search results
    """
    try:
        if not amadeus_tools:
            return {
                "success": False,
                "message": "Amadeus toolkit not available. Please check API credentials.",
                "flights": []
            }
        
        # Find the flight search tool
        flight_tool = None
        for tool in amadeus_tools:
            if "flight" in tool.name.lower() and "search" in tool.name.lower():
                flight_tool = tool
                break
        
        if not flight_tool:
            return {
                "success": False,
                "message": "Flight search tool not found in Amadeus toolkit",
                "flights": []
            }
        
        # Prepare search parameters
        search_params = {
            "origin": origin,
            "destination": destination,
            "departureDate": departure_date,
            "adults": adults,
            "children": children,
            "infants": infants,
            "travelClass": travel_class
        }
        
        if return_date:
            search_params["returnDate"] = return_date
        
        # Execute flight search
        result = flight_tool.invoke(search_params)
        
        return {
            "success": True,
            "message": f"Found flights from {origin} to {destination}",
            "flights": result,
            "search_params": search_params
        }
        
    except Exception as e:
        logger.error(f"Error searching flights: {e}")
        return {
            "success": False,
            "message": f"Error searching flights: {str(e)}",
            "flights": []
        }


@tool
def search_hotels_amadeus(
    city_code: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    rooms: int = 1,
    currency: str = "USD"
) -> Dict[str, Any]:
    """
    Search for hotels using Amadeus API.
    
    Args:
        city_code: City code (e.g., "PAR", "NYC", "LON")
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        adults: Number of adult guests
        rooms: Number of rooms
        currency: Currency code (USD, EUR, GBP, etc.)
        
    Returns:
        Dictionary containing hotel search results
    """
    try:
        if not amadeus_tools:
            return {
                "success": False,
                "message": "Amadeus toolkit not available. Please check API credentials.",
                "hotels": []
            }
        
        # Find the hotel search tool
        hotel_tool = None
        for tool in amadeus_tools:
            if "hotel" in tool.name.lower() and "search" in tool.name.lower():
                hotel_tool = tool
                break
        
        if not hotel_tool:
            return {
                "success": False,
                "message": "Hotel search tool not found in Amadeus toolkit",
                "hotels": []
            }
        
        # Prepare search parameters
        search_params = {
            "cityCode": city_code,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "adults": adults,
            "rooms": rooms,
            "currency": currency
        }
        
        # Execute hotel search
        result = hotel_tool.invoke(search_params)
        
        return {
            "success": True,
            "message": f"Found hotels in {city_code}",
            "hotels": result,
            "search_params": search_params
        }
        
    except Exception as e:
        logger.error(f"Error searching hotels: {e}")
        return {
            "success": False,
            "message": f"Error searching hotels: {str(e)}",
            "hotels": []
        }


@tool
def get_airport_codes_amadeus(city_name: str) -> Dict[str, Any]:
    """
    Get airport codes for a city using Amadeus API.
    
    Args:
        city_name: Name of the city to search for
        
    Returns:
        Dictionary containing airport codes and information
    """
    try:
        if not amadeus_tools:
            return {
                "success": False,
                "message": "Amadeus toolkit not available. Please check API credentials.",
                "airports": []
            }
        
        # Find the airport search tool
        airport_tool = None
        for tool in amadeus_tools:
            if "airport" in tool.name.lower() or "location" in tool.name.lower():
                airport_tool = tool
                break
        
        if not airport_tool:
            return {
                "success": False,
                "message": "Airport search tool not found in Amadeus toolkit",
                "airports": []
            }
        
        # Execute airport search
        result = airport_tool.invoke({"keyword": city_name})
        
        return {
            "success": True,
            "message": f"Found airports for {city_name}",
            "airports": result
        }
        
    except Exception as e:
        logger.error(f"Error searching airports: {e}")
        return {
            "success": False,
            "message": f"Error searching airports: {str(e)}",
            "airports": []
        }


@tool
def get_city_codes_amadeus(city_name: str) -> Dict[str, Any]:
    """
    Get city codes for a city using Amadeus API.
    
    Args:
        city_name: Name of the city to search for
        
    Returns:
        Dictionary containing city codes and information
    """
    try:
        if not amadeus_tools:
            return {
                "success": False,
                "message": "Amadeus toolkit not available. Please check API credentials.",
                "cities": []
            }
        
        # Find the city search tool
        city_tool = None
        for tool in amadeus_tools:
            if "city" in tool.name.lower() and "search" in tool.name.lower():
                city_tool = tool
                break
        
        if not city_tool:
            return {
                "success": False,
                "message": "City search tool not found in Amadeus toolkit",
                "cities": []
            }
        
        # Execute city search
        result = city_tool.invoke({"keyword": city_name})
        
        return {
            "success": True,
            "message": f"Found cities matching {city_name}",
            "cities": result
        }
        
    except Exception as e:
        logger.error(f"Error searching cities: {e}")
        return {
            "success": False,
            "message": f"Error searching cities: {str(e)}",
            "cities": []
        }


@tool
def format_amadeus_results(
    flight_results: Optional[Dict[str, Any]] = None,
    hotel_results: Optional[Dict[str, Any]] = None,
    airport_results: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format Amadeus search results into a readable markdown format.
    
    Args:
        flight_results: Flight search results
        hotel_results: Hotel search results
        airport_results: Airport search results
        
    Returns:
        Formatted markdown string with search results
    """
    markdown_parts = []
    
    if flight_results and flight_results.get("success"):
        markdown_parts.append("## ✈️ Flight Search Results")
        flights = flight_results.get("flights", [])
        if flights:
            for i, flight in enumerate(flights[:5], 1):  # Show top 5 flights
                markdown_parts.append(f"### Flight {i}")
                markdown_parts.append(f"- **Route**: {flight_results['search_params']['origin']} → {flight_results['search_params']['destination']}")
                markdown_parts.append(f"- **Date**: {flight_results['search_params']['departureDate']}")
                if flight_results['search_params'].get('returnDate'):
                    markdown_parts.append(f"- **Return**: {flight_results['search_params']['returnDate']}")
                markdown_parts.append(f"- **Passengers**: {flight_results['search_params']['adults']} adults")
                markdown_parts.append("")
        else:
            markdown_parts.append("No flights found for the specified criteria.")
    
    if hotel_results and hotel_results.get("success"):
        markdown_parts.append("## 🏨 Hotel Search Results")
        hotels = hotel_results.get("hotels", [])
        if hotels:
            for i, hotel in enumerate(hotels[:5], 1):  # Show top 5 hotels
                markdown_parts.append(f"### Hotel {i}")
                markdown_parts.append(f"- **Location**: {hotel_results['search_params']['cityCode']}")
                markdown_parts.append(f"- **Check-in**: {hotel_results['search_params']['checkInDate']}")
                markdown_parts.append(f"- **Check-out**: {hotel_results['search_params']['checkOutDate']}")
                markdown_parts.append(f"- **Guests**: {hotel_results['search_params']['adults']} adults, {hotel_results['search_params']['rooms']} rooms")
                markdown_parts.append("")
        else:
            markdown_parts.append("No hotels found for the specified criteria.")
    
    if airport_results and airport_results.get("success"):
        markdown_parts.append("## 🛫 Airport Information")
        airports = airport_results.get("airports", [])
        if airports:
            for airport in airports[:3]:  # Show top 3 airports
                markdown_parts.append(f"- **{airport.get('name', 'Unknown')}** ({airport.get('iataCode', 'N/A')})")
                markdown_parts.append(f"  - {airport.get('address', {}).get('cityName', 'Unknown City')}, {airport.get('address', {}).get('countryName', 'Unknown Country')}")
        else:
            markdown_parts.append("No airports found for the specified criteria.")
    
    if not markdown_parts:
        return "No search results available."
    
    return "\n".join(markdown_parts)


# Export the Amadeus tools for use in agents
amadeus_travel_tools = [
    search_flights_amadeus,
    search_hotels_amadeus,
    get_airport_codes_amadeus,
    get_city_codes_amadeus,
    format_amadeus_results
]
