# Useful Commands

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
