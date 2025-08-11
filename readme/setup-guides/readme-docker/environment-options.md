# Environment Options

### Development Environment

```bash
# Start development environment
./scripts/docker-setup.sh development

# Or manually
docker-compose -f docker-compose.dev.yml up --build
```

**Features:**

* Django development server with auto-reload
* Debug mode enabled
* pgAdmin for database management
* Additional debugging tools (ipython, ipdb, django-debug-toolbar)

### Production Environment

```bash
# Start production environment
./scripts/docker-setup.sh production

# Or manually
docker-compose up --build
```

**Features:**

* Gunicorn WSGI server
* Nginx reverse proxy
* Static file serving
* Rate limiting
* Security headers
* Gzip compression

### Test Environment

```bash
# Run tests
./scripts/docker-setup.sh test

# Or manually
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

**Features:**

* Isolated test database
* Coverage reporting
* Automated test execution
