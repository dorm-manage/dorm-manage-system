# Local and Docker Setup Guide

Welcome to the DormitoriesPlus setup guide! This document will walk you through setting up the application both locally and using Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Setup](#docker-setup)
- [Translation Support](#translation-support)
- [Troubleshooting](#troubleshooting)
- [Development Workflow](#development-workflow)

## Prerequisites

Before you begin, ensure you have the following installed:

### For Local Development
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer
- **Git** - [Download Git](https://git-scm.com/downloads)
- **PostgreSQL** (optional, SQLite is used by default)

### For Docker Setup
- **Docker Desktop** - [Download Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose** - Usually included with Docker Desktop

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

## Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DB_NAME=dormitoriesplus
DB_USER=dorm_user
DB_PASSWORD=dorm_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Compile Translations

```bash
# Compile all supported languages
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
```

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Your application is now running at `http://localhost:8000`

## Docker Setup

### Quick Start with Docker

The easiest way to run the application is using Docker. We provide automated scripts for setup.

### Option 1: Automated Setup (Recommended)

```bash
# Development mode
./scripts/docker-translation-setup.sh dev

# Production mode
./scripts/docker-translation-setup.sh
```

### Option 2: Manual Docker Setup

#### Step 1: Build and Start Containers

```bash
# Build and start all services
docker-compose up --build
```

#### Step 2: Access the Application

- **Development**: http://localhost:8080
- **Production**: http://localhost:80

### Option 3: Update with Latest Changes

If you've made changes to translations or code:

```bash
./scripts/update-docker-translations.sh
```

## Translation Support

### Supported Languages

The application supports multiple languages:

- **Hebrew (עברית)** - Default language
- **English** - Secondary language
- **Arabic (العربية)** - RTL support
- **Chinese (中文)** - Simplified Chinese

### Translation Management

#### Compile Translations

```bash
# Local development
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv

# Docker
docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
```

#### Create New Translations

```bash
# Local development
python manage.py makemessages -l he -l en -l ar -l zh

# Docker
docker-compose exec web python manage.py makemessages -l he -l en -l ar -l zh
```

#### Update Existing Translations

```bash
# Local development
python manage.py makemessages -a

# Docker
docker-compose exec web python manage.py makemessages -a
```

### Testing Translations

```bash
# Test Docker translation setup
./scripts/test-docker-translations.sh
```

## Development Workflow

### Local Development

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Make changes** to your code or templates

3. **Test changes** in your browser at `http://localhost:8000`

4. **For translation changes**:
   ```bash
   python manage.py makemessages -a
   # Edit .po files in locale/ directory
   python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
   ```

### Docker Development

1. **Start containers**:
   ```bash
   docker-compose up --build
   ```

2. **Make changes** to your code or templates

3. **Rebuild containers** (if needed):
   ```bash
   docker-compose up --build
   ```

4. **For translation changes**:
   ```bash
   docker-compose exec web python manage.py makemessages -a
   # Edit .po files in locale/ directory
   docker-compose exec web python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
   ```

## Troubleshooting

### Common Issues

#### Local Development Issues

**Issue**: `ModuleNotFoundError: No module named 'django'`
```bash
# Solution: Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Issue**: `Database connection failed`
```bash
# Solution: Check database settings in .env file
# For SQLite (default), ensure the database file is writable
```

**Issue**: `Translation compilation warnings`
```bash
# Solution: These are expected for Django built-in strings
# Custom translations will work correctly despite warnings
```

#### Docker Issues

**Issue**: `Docker is not running`
```bash
# Solution: Start Docker Desktop
# On macOS: Open Docker Desktop application
# On Windows: Start Docker Desktop from Start menu
# On Linux: sudo systemctl start docker
```

**Issue**: `Port already in use`
```bash
# Solution: Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

**Issue**: `Permission denied`
```bash
# Solution: Ensure Docker has proper permissions
# On Linux: sudo usermod -aG docker $USER
```

### Performance Optimization

#### Local Development
- Use `DEBUG=True` for development
- Enable Django Debug Toolbar for performance monitoring
- Use SQLite for faster development setup

#### Docker Development
- Use volume mounts for faster file changes
- Enable Docker BuildKit for faster builds
- Use multi-stage builds for production

### Debugging

#### Local Development
```bash
# Enable debug mode
export DEBUG=True

# Run with debug output
python manage.py runserver --verbosity=2
```

#### Docker Development
```bash
# View container logs
docker-compose logs web

# Access container shell
docker-compose exec web bash

# Check translation files
docker-compose exec web ls -la locale/*/LC_MESSAGES/
```

## Environment Variables

### Required Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DB_NAME` | Database name | `dormitoriesplus` |
| `DB_USER` | Database user | `dorm_user` |
| `DB_PASSWORD` | Database password | `dorm_password` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_HOST_USER` | Email username | None |
| `EMAIL_HOST_PASSWORD` | Email password | None |
| `DEFAULT_FROM_EMAIL` | Default sender email | None |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |

## File Structure

```
dorm-manage-system/
├── DormitoriesPlus/           # Main Django app
├── DormitoriesPlus_project/   # Django project settings
├── templates/                 # HTML templates
│   ├── BM_pages/             # Building Manager pages
│   ├── OM_pages/             # Office Manager pages
│   └── Student_pages/        # Student pages
├── locale/                   # Translation files
│   ├── he/LC_MESSAGES/      # Hebrew translations
│   ├── en/LC_MESSAGES/      # English translations
│   ├── ar/LC_MESSAGES/      # Arabic translations
│   └── zh/LC_MESSAGES/      # Chinese translations
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User-uploaded files
├── scripts/                  # Setup and utility scripts
├── docker-compose.yml        # Docker configuration
├── Dockerfile               # Docker image definition
└── requirements.txt         # Python dependencies
```

## Next Steps

After setting up the application:

1. **Explore the interface** at `http://localhost:8000` (local) or `http://localhost:8080` (Docker)
2. **Create test data** using the admin interface
3. **Test different user roles** (Student, Building Manager, Office Manager)
4. **Explore translation features** by switching languages
5. **Review the API documentation** for integration options

## Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review the logs** for error messages
3. **Ensure all prerequisites** are installed correctly
4. **Check the GitHub issues** for known problems
5. **Create a new issue** if the problem persists

---

**Happy coding! 🚀** 