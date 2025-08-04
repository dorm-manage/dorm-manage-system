#!/bin/bash

# Test Docker Translation Setup
# This script tests if translations are working properly in Docker

echo "🧪 Testing Docker translation setup..."

# Check if containers are running
if ! docker-compose ps | grep -q "web.*Up"; then
    echo "❌ Web container is not running. Please start Docker first:"
    echo "   ./scripts/docker-translation-setup.sh dev"
    exit 1
fi

echo "✅ Containers are running"

# Test translation compilation
echo "📝 Testing translation compilation..."
docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh

if [ $? -eq 0 ]; then
    echo "✅ Translation compilation successful"
else
    echo "❌ Translation compilation failed"
    exit 1
fi

# Test if .mo files exist
echo "🔍 Checking for compiled translation files..."
for lang in he en ar zh; do
    if [ -f "locale/$lang/LC_MESSAGES/django.mo" ]; then
        echo "✅ $lang translation file exists"
    else
        echo "❌ $lang translation file missing"
        exit 1
    fi
done

# Test web server response
echo "🌐 Testing web server response..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080)

if [ "$response" = "302" ] || [ "$response" = "200" ]; then
    echo "✅ Web server responding correctly (HTTP $response)"
else
    echo "❌ Web server not responding correctly (HTTP $response)"
    exit 1
fi

echo ""
echo "🎉 All translation tests passed!"
echo ""
echo "🌐 Your Docker setup now supports:"
echo "   - Hebrew (עברית)"
echo "   - English"
echo "   - Arabic (العربية)"
echo "   - Chinese (中文)"
echo ""
echo "📱 Access your application at:"
echo "   - Development: http://localhost:8080"
echo "   - Production: http://localhost:80" 