# Quick Start Guide

Get up and running with DormitoriesPlus in minutes!

## 🚀 Quick Start Options

### Option 1: Docker (Recommended)

**Prerequisites**: Docker Desktop

```bash
# Clone the repository
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system

# Start with Docker (Development mode)
./scripts/docker-translation-setup.sh dev

# Access the application
# Open http://localhost:8080 in your browser
```

### Option 2: Local Development

**Prerequisites**: Python 3.8+, pip, Git

```bash
# Clone the repository
git clone https://github.com/your-username/dorm-manage-system.git
cd dorm-manage-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env  # Create environment file
python manage.py migrate
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver

# Access the application
# Open http://localhost:8000 in your browser
```

## 🌐 Translation Support

The application supports multiple languages:

- **Hebrew (עברית)** - Default
- **English**
- **Arabic (العربية)**
- **Chinese (中文)**

### Testing Translations

```bash
# Test Docker setup
./scripts/test-docker-translations.sh

# Update translations
./scripts/update-docker-translations.sh
```

## 🔧 Common Commands

### Docker Commands

```bash
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

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Compile translations
python manage.py compilemessages --locale=he --locale=en --locale=ar --locale=zh --ignore=venv

# Collect static files
python manage.py collectstatic --noinput
```

## 🐛 Troubleshooting

### Docker Issues

**Docker not running**
```bash
# Start Docker Desktop application
# Then run: docker-compose up --build
```

**Port conflicts**
```bash
# Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

### Local Issues

**Module not found**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Translation warnings**
```bash
# These are expected for Django built-in strings
# Custom translations work correctly despite warnings
```

## 📱 Access Points

- **Local Development**: http://localhost:8000
- **Docker Development**: http://localhost:8080
- **Docker Production**: http://localhost:80

## 🎯 Next Steps

1. **Explore the interface** and test different user roles
2. **Create test data** using the admin interface
3. **Test translation features** by switching languages
4. **Review the full documentation** for advanced features

---

**Need help?** Check the [full setup guide](local-and-docker-setup.md) or [create an issue](https://github.com/your-username/dorm-manage-system/issues). 