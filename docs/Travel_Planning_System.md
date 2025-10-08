# 🌍 Travel Planning System Documentation

## Overview

The Travel Planning System is a comprehensive multi-agent AI platform designed to help users plan their perfect trips. It combines specialized travel agents with real-time API integrations and vector database search capabilities to provide end-to-end travel planning assistance.

## 🏗️ System Architecture

### Multi-Agent Architecture

```
Travel Planning System
├── Travel Planning Agent (Main Coordinator)
├── Travel Destination Agent (Destination Research)
├── Travel Package Agent (Package Search & Booking)
├── Travel Supervisor Agent (Workflow Coordination)
└── Vector Database (Destination Knowledge Base)
```

### Core Components

1. **Travel Planning Agent** - Main coordinator that orchestrates the entire travel planning process
2. **Travel Destination Agent** - Specialized in destination research and insights
3. **Travel Package Agent** - Handles package search and booking assistance
4. **Travel Supervisor Agent** - Coordinates workflow between specialized agents
5. **Vector Database** - Stores and searches travel destination information

## 🛠️ Features

### Destination Research

- **Vector-based Search**: Semantic search through 6,000+ travel destinations
- **Comprehensive Information**: Detailed destination data including attractions, activities, and travel tips
- **Similarity Matching**: Find destinations similar to user preferences
- **Criteria-based Filtering**: Search by country, region, activity type, and travel season

### Travel Planning

- **End-to-end Planning**: Complete trip planning from destination selection to booking
- **Real-time Data**: Integration with travel APIs for current information
- **Package Search**: Find and compare travel packages
- **Airport Information**: Get relevant airports and transportation options
- **Date Planning**: Calculate optimal travel dates and duration

### User Interface

- **Streamlit Widget**: Interactive travel planning form
- **Markdown Responses**: Beautifully formatted travel recommendations
- **Chat Integration**: Natural language interaction with travel agents
- **Guided Experience**: Step-by-step travel planning workflow

## 📊 Data Sources

### Vector Database

- **Source**: CSV file with 6,000+ travel destinations
- **Embeddings**: Pre-generated vector embeddings for semantic search
- **Metadata**: Rich destination information including:
  - Destination name and description
  - Famous attractions and landmarks
  - Unique offerings and activities
  - Region and country information
  - Best time to travel
  - Cultural characteristics

### External APIs

- **Airport Search**: `https://api.tratoli.com/api/airports/`
- **Package Booking**: `https://apistagging.tratoli.com/api/unified-package`
- **Real-time Data**: Current flight and hotel information

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Required Python packages (see `pyproject.toml`)

### Setup

1. **Create Vector Database**:

   ```bash
   python scripts/create_travel_vector_db.py
   ```

2. **Start the Service**:

   ```bash
   python src/run_service.py
   ```

3. **Launch Streamlit App**:
   ```bash
   streamlit run src/streamlit_app.py
   ```

### Usage

#### Via Streamlit Widget

1. Click "🌍 Travel Planning" in the sidebar
2. Fill out the travel planning form
3. Click "🚀 Plan My Trip"
4. Review the comprehensive travel recommendation

#### Via Chat Interface

1. Select "travel-planning-agent" from the agent dropdown
2. Ask questions like:
   - "Plan a trip to Paris for 7 days"
   - "Find beach destinations in Europe"
   - "Search for cultural cities in Asia"

## 🔧 Configuration

### Environment Variables

```bash
# Travel API Configuration
TRAVEL_API_BASE=https://api.tratoli.com
PACKAGE_API_BASE=https://apistagging.tratoli.com
TRAVEL_TOKEN=your_travel_api_token

# Vector Database
VECTOR_DB_PATH=./travel_vector_db
```

### Agent Configuration

The travel agents are configured in `src/agents/agents.py`:

- `travel-planning-agent`: Main comprehensive agent
- `travel-destination-agent`: Destination research specialist
- `travel-package-agent`: Package search specialist
- `travel-supervisor-agent`: Workflow coordinator

## 📝 API Reference

### Travel Tools

#### `search_destinations_vector(query, n_results=5)`

Search for destinations using vector similarity.

**Parameters:**

- `query`: Search query (e.g., "beach destinations")
- `n_results`: Number of results to return

**Returns:**

- List of matching destinations with similarity scores

#### `get_destination_by_name(destination_name)`

Get detailed information about a specific destination.

**Parameters:**

- `destination_name`: Name of the destination

**Returns:**

- Detailed destination information

#### `search_travel_packages(destination, start_date, ...)`

Search for available travel packages.

**Parameters:**

- `destination`: Destination city/country
- `start_date`: Start date in DD/MM/YYYY format
- `duration_days`: Trip duration
- `adults`: Number of adults
- `children`: Number of children
- `hotel_star`: Preferred hotel rating

**Returns:**

- Available travel packages

#### `search_airports(city_name)`

Search for airports by city name.

**Parameters:**

- `city_name`: Name of the city

**Returns:**

- List of airports with IATA codes

## 🎯 Use Cases

### 1. Destination Discovery

- "Find beach destinations in Southeast Asia"
- "Show me cultural cities in Europe"
- "What are the best adventure destinations?"

### 2. Trip Planning

- "Plan a 10-day trip to Japan for 2 adults"
- "Find family-friendly destinations in Europe"
- "Search for luxury travel packages to the Maldives"

### 3. Travel Research

- "What's the best time to visit Iceland?"
- "Tell me about attractions in Barcelona"
- "Find destinations similar to Santorini"

### 4. Booking Assistance

- "Help me book a package to Thailand"
- "Find flights from Mumbai to Paris"
- "Search for 5-star hotels in Dubai"

## 🔍 Advanced Features

### Vector Search Capabilities

- **Semantic Understanding**: Find destinations based on meaning, not just keywords
- **Multi-criteria Search**: Combine multiple search criteria
- **Similarity Matching**: Find destinations similar to user preferences
- **Contextual Results**: Results ranked by relevance and similarity

### Multi-Agent Coordination

- **Workflow Management**: Coordinated execution across specialized agents
- **Information Synthesis**: Combine data from multiple sources
- **Quality Assurance**: Ensure comprehensive and accurate recommendations
- **User Experience**: Seamless interaction across all agents

### Real-time Integration

- **Live Data**: Current flight and hotel availability
- **Dynamic Pricing**: Real-time package pricing
- **Availability Checking**: Current booking status
- **API Integration**: Seamless connection to travel services

## 🚨 Error Handling

### Common Issues

1. **Vector Database Not Found**: Run the setup script to create the database
2. **API Connection Issues**: Check network connectivity and API credentials
3. **Agent Loading Errors**: Ensure all dependencies are installed
4. **Memory Issues**: Monitor system resources for large vector operations

### Troubleshooting

- Check logs for detailed error messages
- Verify API credentials and network connectivity
- Ensure vector database is properly initialized
- Monitor system resources during operation

## 🔮 Future Enhancements

### Planned Features

- **Real-time Flight Search**: Integration with flight booking APIs
- **Hotel Recommendations**: Advanced hotel search and booking
- **Itinerary Generation**: Automated day-by-day itinerary creation
- **Price Alerts**: Monitor price changes for travel packages
- **Social Features**: Share and collaborate on travel plans
- **Mobile App**: Native mobile application
- **Voice Interface**: Voice-activated travel planning
- **AR/VR Integration**: Virtual destination previews

### Technical Improvements

- **Performance Optimization**: Faster vector search and response times
- **Caching Layer**: Improved response caching for better performance
- **Multi-language Support**: Support for multiple languages
- **Advanced Analytics**: Travel pattern analysis and insights
- **Machine Learning**: Personalized recommendations based on user history

## 📞 Support

For technical support or questions about the Travel Planning System:

- **Email**: travel@investmentadvisory.com
- **Documentation**: Check this documentation and inline code comments
- **Issues**: Report bugs and feature requests through the project repository

## 📄 License

This Travel Planning System is part of the Investment Advisory AI Platform and is licensed under the same terms as the main project.
