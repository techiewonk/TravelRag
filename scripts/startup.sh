#!/bin/bash
set -e

echo "Starting TravelRag service with ChromaDB setup..."

# Check if ChromaDB needs to be seeded
echo "Checking ChromaDB status..."
python scripts/seed_chromadb.py

# Start the main service
echo "Starting main service..."
exec "$@"
