# 🐳 Docker ChromaDB Setup Guide

## Overview

This guide explains how ChromaDB is integrated into the Docker setup for the TravelRag application. The ChromaDB vector database is automatically seeded with travel destination data when the container starts.

## 🏗️ Architecture

### Docker Components

1. **ChromaDB Volume**: Persistent storage for the vector database
2. **Seeding Script**: Automatically populates ChromaDB with travel data
3. **Startup Script**: Orchestrates the seeding and service startup
4. **Service Integration**: ChromaDB tools are available in the agent service

### File Structure

```
├── compose.yaml                    # Docker Compose configuration
├── docker/
│   ├── Dockerfile.service         # Service container with ChromaDB
│   └── Dockerfile.app             # Streamlit app container
├── scripts/
│   ├── seed_chromadb.py           # ChromaDB seeding script
│   ├── startup.sh                 # Container startup script
│   └── test_docker_chromadb.py    # Docker ChromaDB test
└── src/agents/
    └── chroma_travel_tools.py     # ChromaDB travel tools
```

## 🚀 Quick Start

### 1. Start the Services

```bash
# Start all services including ChromaDB
docker compose up -d

# Or start with build
docker compose up --build -d
```

### 2. Verify ChromaDB Setup

```bash
# Check if ChromaDB was seeded successfully
docker compose exec agent_service python scripts/test_docker_chromadb.py
```

### 3. Access the Services

- **Agent Service**: http://localhost:8080
- **Streamlit App**: http://localhost:8501
- **PostgreSQL**: localhost:5432

## 📊 ChromaDB Features

### Automatic Seeding

The ChromaDB database is automatically seeded when the container starts:

- ✅ **Smart Detection**: Only seeds if database is empty
- ✅ **Data Source**: Uses `documents_rows.csv` (826 destinations)
- ✅ **Vector Embeddings**: Automatically generated
- ✅ **Persistent Storage**: Data persists between container restarts

### Available Tools

The following ChromaDB tools are available in the agent service:

```python
# Semantic search
search_destinations_chroma("beach destinations", n_results=5)

# Exact destination lookup
get_destination_by_name_chroma("Paris")

# Criteria-based search
search_destinations_by_criteria_chroma(
    country="France",
    region="Europe",
    activity_type="cultural",
    n_results=10
)

# Database statistics
get_database_stats_chroma()
```

## 🔧 Configuration

### Environment Variables

The ChromaDB setup uses the following paths:

- **Docker**: `/app/travel_chromadb`
- **Local**: `./travel_chromadb`
- **Data Source**: `/app/documents_rows.csv`

### Volume Mounting

```yaml
volumes:
  - travel_chromadb_data:/app/travel_chromadb
```

The ChromaDB data is stored in a named Docker volume for persistence.

## 🧪 Testing

### Test ChromaDB in Docker

```bash
# Run the Docker ChromaDB test
docker compose exec agent_service python scripts/test_docker_chromadb.py
```

### Test ChromaDB Tools

```bash
# Test semantic search
docker compose exec agent_service python -c "
from src.agents.chroma_travel_tools import search_destinations_chroma
result = search_destinations_chroma('beach destinations', 3)
print(f'Found {len(result[\"destinations\"])} destinations')
"
```

## 🔄 Development Workflow

### Rebuilding with ChromaDB Changes

```bash
# Rebuild and restart services
docker compose down
docker compose up --build -d
```

### Viewing Logs

```bash
# View agent service logs (includes ChromaDB seeding)
docker compose logs -f agent_service

# View specific ChromaDB seeding logs
docker compose logs agent_service | grep -i chroma
```

### Resetting ChromaDB

```bash
# Remove ChromaDB volume and restart
docker compose down -v
docker compose up -d
```

## 📈 Performance

### Database Statistics

The seeded ChromaDB contains:

- **826 destinations** from CSV data
- **55 unique countries**
- **82 unique regions**
- **~7MB** database size
- **Vector embeddings** for semantic search

### Query Performance

- **Semantic Search**: ~100-500ms per query
- **Exact Lookup**: ~50-200ms per query
- **Criteria Search**: ~200-800ms per query

## 🐛 Troubleshooting

### Common Issues

#### 1. ChromaDB Not Seeding

```bash
# Check if CSV file exists
docker compose exec agent_service ls -la /app/documents_rows.csv

# Check seeding logs
docker compose logs agent_service | grep -i "seeding\|chroma"
```

#### 2. Permission Issues

```bash
# Fix script permissions
docker compose exec agent_service chmod +x scripts/startup.sh
```

#### 3. Volume Issues

```bash
# Check volume status
docker volume ls | grep travel_chromadb

# Inspect volume
docker volume inspect travelrag_travel_chromadb_data
```

### Debug Mode

```bash
# Run container in debug mode
docker compose exec agent_service bash

# Inside container, test ChromaDB manually
python scripts/seed_chromadb.py
python scripts/test_docker_chromadb.py
```

## 🔒 Security

### Data Protection

- ChromaDB data is stored in Docker volumes
- No external network access required for ChromaDB
- Data is isolated within the container environment

### Access Control

- ChromaDB is only accessible from within the agent service container
- No direct external access to the vector database
- All access is through the agent service API

## 📚 Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Travel Tools API Reference](../src/agents/chroma_travel_tools.py)

---

**Note**: The ChromaDB setup is designed to be production-ready with automatic seeding, persistent storage, and comprehensive error handling.
