# Troubleshooting

### Common Issues

1.  **Port already in use**

    ```bash
    # Check what's using the port
    lsof -i :8000

    # Stop conflicting service or change port in docker-compose.yml
    ```
2.  **Database connection issues**

    ```bash
    # Check if database is running
    docker-compose ps db

    # Check database logs
    docker-compose logs db
    ```
3.  **Permission issues**

    ```bash
    # Fix file permissions
    sudo chown -R $USER:$USER .
    ```
4.  **Build failures**

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
