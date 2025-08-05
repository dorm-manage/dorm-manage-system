#!/bin/bash

# Update Docker with Latest Translations Script
# This script updates Docker with our latest translation work

echo "🔄 Updating Docker with latest translations..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images to ensure fresh build
echo "🧹 Cleaning up old images..."
docker-compose down --rmi all

# Build and start with latest translations
echo "🔨 Building with latest translations..."
docker-compose up --build -d

# Wait for containers to start
echo "⏳ Waiting for containers to start..."
sleep 10

# Test the setup
echo "🧪 Testing the updated setup..."
./scripts/test-docker-translations.sh

echo ""
echo "✅ Docker update complete!"
echo "📱 Your application is now running with the latest translations at:"
echo "   - Development: http://localhost:8080"
echo "   - Production: http://localhost:80"
echo ""
echo "🌐 Updated translation support includes:"
echo "   - Hebrew (עברית) - Default"
echo "   - English"
echo "   - Arabic (العربية)"
echo "   - Chinese (中文)"
echo ""
echo "📝 Note: Some Django built-in translation warnings are expected and don't affect functionality." 