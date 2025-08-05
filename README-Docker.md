# Docker Setup for DormitoriesPlus

This document provides instructions for running the DormitoriesPlus application using Docker.

## 🐳 Quick Start

### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

### Quick Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd dorm-manage-system
   ```

2. **Run the translation setup script**:
   ```bash
   ./scripts/docker-translation-setup.sh dev
   ```

3. **Access the application**:
   - Main application: http://localhost:8080
   - pgAdmin (database management): http://localhost:5050
   - Production: http://localhost:80

## 📁 Docker Files Overview

### Core Files
- `Dockerfile` - Production Docker image
- `Dockerfile.dev` - Development Docker image with debugging tools
- `docker-compose.yml` - Production environment with nginx
- `docker-compose.dev.yml` - Development environment
- `docker-compose.test.yml` - Test environment
- `nginx.conf` - Nginx configuration for production
- `.dockerignore` - Files to exclude from Docker build

## 🚀 Environment Options

### Development Environment
```bash
# Start development environment
./scripts/docker-setup.sh development

# Or manually
docker-compose -f docker-compose.dev.yml up --build
```

**Features:**
- Django development server with auto-reload
- Debug mode enabled
- pgAdmin for database management
- Additional debugging tools (ipython, ipdb, django-debug-toolbar)

### Production Environment
```bash
# Start production environment
./scripts/docker-setup.sh production

# Or manually
docker-compose up --build
```

**Features:**
- Gunicorn WSGI server
- Nginx reverse proxy
- Static file serving
- Rate limiting
- Security headers
- Gzip compression

### Test Environment
```bash
# Run tests
./scripts/docker-setup.sh test

# Or manually
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

**Features:**
- Isolated test database
- Coverage reporting
- Automated test execution

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database settings
DB_NAME=dormitoriesplus
DB_USER=dorm_user
DB_PASSWORD=dorm_password
DB_HOST=db
DB_PORT=5432

# Email settings (for production)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=dormitoriesplus.notifications@gmail.com

# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### Database Configuration

The application uses PostgreSQL with the following default settings:
- **Database**: dormitoriesplus
- **User**: dorm_user
- **Password**: dorm_password
- **Host**: db (container name)
- **Port**: 5432

### Redis Configuration

Redis is used for caching and session storage:
- **Host**: redis (container name)
- **Port**: 6379

## 📊 Services

### Web Application
- **Port**: 8080 (development) / 80 (production via nginx)
- **Framework**: Django 3.1.12
- **WSGI Server**: Gunicorn (production)
- **Development Server**: Django runserver (development)

### Database
- **Service**: PostgreSQL 13
- **Port**: 5432
- **Volume**: postgres_data (persistent storage)

### Cache
- **Service**: Redis 6
- **Port**: 6379
- **Volume**: redis_data (persistent storage)

### Web Server (Production)
- **Service**: Nginx
- **Port**: 80
- **Features**: Reverse proxy, static file serving, rate limiting

### Database Management (Development)
- **Service**: pgAdmin 4
- **Port**: 5050
- **Credentials**: admin@dormitoriesplus.com / admin123

## 🛠️ Useful Commands

### Basic Operations
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Rebuild containers
docker-compose up --build

# Remove volumes (WARNING: deletes all data)
docker-compose down -v
```

### Development Commands
```bash
# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run tests
docker-compose exec web python manage.py test
```

### Database Commands
```bash
# Access PostgreSQL
docker-compose exec db psql -U dorm_user -d dormitoriesplus

# Backup database
docker-compose exec db pg_dump -U dorm_user dormitoriesplus > backup.sql

# Restore database
docker-compose exec -T db psql -U dorm_user -d dormitoriesplus < backup.sql
```

### Container Management
```bash
# List running containers
docker ps

# Access container shell
docker-compose exec web bash

# View container resources
docker stats

# Clean up unused containers/images
docker system prune
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Stop conflicting service or change port in docker-compose.yml
   ```

2. **Database connection issues**
   ```bash
   # Check if database is running
   docker-compose ps db
   
   # Check database logs
   docker-compose logs db
   ```

3. **Permission issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

4. **Build failures**
   ```bash
   # Clean build cache
   docker-compose build --no-cache
   ```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f web

# View container details
docker-compose ps
docker inspect <container_name>
```

## 📈 Performance Optimization

### Production Optimizations
- Use multiple Gunicorn workers
- Enable nginx caching
- Configure Redis for session storage
- Use CDN for static files
- Enable database connection pooling

### Development Optimizations
- Mount source code as volume for live reload
- Use volume caching for pip dependencies
- Enable Django debug toolbar
- Use separate development database

## 🔒 Security Considerations

### Production Security
- Change default passwords
- Use strong SECRET_KEY
- Enable HTTPS
- Configure proper firewall rules
- Regular security updates
- Database backups

### Development Security
- Use separate development database
- Don't commit sensitive data
- Use environment variables for secrets
- Regular dependency updates

## 🌐 Internationalization Support

### Supported Languages
The Docker setup includes full internationalization support for:
- **Hebrew (עברית)** - Default language
- **English** - Secondary language
- **Arabic (العربية)** - RTL support
- **Chinese (中文)** - Simplified Chinese

### Translation Features
- **Automatic compilation** of `.po` files during Docker build
- **Runtime language switching** via URL parameters or cookies
- **RTL layout support** for Hebrew and Arabic
- **Unicode support** for all languages
- **Fallback handling** for missing translations

### Translation Management
```bash
# Compile translations manually (if needed)
docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh

# Create new translation files
docker-compose exec web python manage.py makemessages -l he -l en -l ar -l zh

# Update existing translations
docker-compose exec web python manage.py makemessages -a
```

### Language Switching
Users can switch languages by:
1. **URL parameter**: `?lang=en`
2. **Cookie setting**: `django_language=en`
3. **Browser language detection** (automatic)

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment](https://docs.djangoproject.com/en/3.1/howto/deployment/)
- [Django Internationalization](https://docs.djangoproject.com/en/3.1/topics/i18n/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Nginx Documentation](https://nginx.org/en/docs/) 