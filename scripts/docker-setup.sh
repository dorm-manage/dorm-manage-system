#!/bin/bash

# Docker setup script for DormitoriesPlus
set -e

echo "🐳 Setting up Docker for DormitoriesPlus..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database settings
DB_NAME=dormitoriesplus
DB_USER=dorm_user
DB_PASSWORD=dorm_password
DB_HOST=db
DB_PORT=5432

# Email settings (optional - for production)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=dormitoriesplus.notifications@gmail.com

# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=False
EOF
    echo "✅ Created .env file. Please update it with your actual values."
fi

# Function to build and start services
start_services() {
    local compose_file=$1
    local service_name=$2
    
    echo "🔨 Building and starting $service_name..."
    docker-compose -f $compose_file up --build -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo "✅ $service_name is ready!"
    echo "🌐 Access your application at: http://localhost:8080"
    echo "🗄️  Database is available at: localhost:5432"
    echo "🔴 Redis is available at: localhost:6379"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [production|development|test]"
    echo ""
    echo "Options:"
    echo "  production   - Start production environment with nginx"
    echo "  development  - Start development environment with debugging tools"
    echo "  test         - Run tests in isolated environment"
    echo ""
    echo "Examples:"
    echo "  $0 production"
    echo "  $0 development"
    echo "  $0 test"
}

# Main script logic
case "${1:-development}" in
    production)
        echo "🚀 Starting production environment..."
        start_services "docker-compose.yml" "production services"
        echo "📊 pgAdmin is available at: http://localhost:5050"
        ;;
    development)
        echo "🔧 Starting development environment..."
        start_services "docker-compose.dev.yml" "development services"
        echo "📊 pgAdmin is available at: http://localhost:5050"
        ;;
    test)
        echo "🧪 Running tests..."
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
        echo "✅ Tests completed!"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f web          # View application logs"
echo "  docker-compose exec web python manage.py shell  # Access Django shell"
echo "  docker-compose exec db psql -U dorm_user -d dormitoriesplus  # Access database"
echo "  docker-compose down                 # Stop all services"
echo "  docker-compose down -v              # Stop and remove volumes" 