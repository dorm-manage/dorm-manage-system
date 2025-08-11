# Common Commands

### Docker Commands

```
# Start development environment
docker-compose up --build

# Stop containers
docker-compose down

# View logs
docker-compose logs web

# Access container shell
docker-compose exec web bash
```

### Local Development Commands

```
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Compile translations
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv

# Collect static files
python manage.py collectstatic --noinput
```
