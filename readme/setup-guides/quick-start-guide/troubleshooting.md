# Troubleshooting

### Docker issues

**Docker not running**

```
# Start Docker Desktop application
# Then run: docker-compose up --build
```

**Port conflicts**

```
# Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

### Local issues

**Module not found**

```
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Translation warnings

```
# These are expected for Django built-in strings
# Custom translations work correctly despite warnings
```
