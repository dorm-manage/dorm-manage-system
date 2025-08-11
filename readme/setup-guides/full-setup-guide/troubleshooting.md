# Troubleshooting

## Common Issues

### **Local Development Issues**

**Issue**: `ModuleNotFoundError: No module named 'django'`

```
# Solution: Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Issue**: `Database connection failed`

```
# Solution: Check database settings in .env file
# For SQLite (default), ensure the database file is writable
```

**Issue**: `Translation compilation warnings`

```
# Solution: These are expected for Django built-in strings
# Custom translations will work correctly despite warnings
```



### **Docker Issues**

**Issue**: `Docker is not running`

```
# Solution: Start Docker Desktop
# On macOS: Open Docker Desktop application
# On Windows: Start Docker Desktop from Start menu
# On Linux: sudo systemctl start docker
```

**Issue**: `Port already in use`

```
# Solution: Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

**Issue**: `Permission denied`

```
# Solution: Ensure Docker has proper permissions
# On Linux: sudo usermod -aG docker $USER
```



## Performance Optimization

### **Local Development**

* Use `DEBUG=True` for development
* Enable Django Debug Toolbar for performance monitoring
* Use SQLite for faster development setup



### **Docker Development**

* Use volume mounts for faster file changes
* Enable Docker BuildKit for faster builds
* Use multi-stage builds for production



## Debugging

### **Local Development**

```
# Enable debug mode
export DEBUG=True

# Run with debug output
python manage.py runserver --verbosity=2
```



### **Docker Development**

```
# View container logs
docker-compose logs web

# Access container shell
docker-compose exec web bash

# Check translation files
docker-compose exec web ls -la locale/*/LC_MESSAGES/
```
