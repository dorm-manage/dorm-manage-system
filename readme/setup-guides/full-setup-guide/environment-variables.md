# Environment Variables

### Required Variables

| Variable      | Description       | Default           |
| ------------- | ----------------- | ----------------- |
| `DEBUG`       | Enable debug mode | `False`           |
| `SECRET_KEY`  | Django secret key | Auto-generated    |
| `DB_NAME`     | Database name     | `dormitoriesplus` |
| `DB_USER`     | Database user     | `dorm_user`       |
| `DB_PASSWORD` | Database password | `dorm_password`   |
| `DB_HOST`     | Database host     | `localhost`       |
| `DB_PORT`     | Database port     | `5432`            |



### Optional Variables

| Variable              | Description          | Default                    |
| --------------------- | -------------------- | -------------------------- |
| `EMAIL_HOST_USER`     | Email username       | None                       |
| `EMAIL_HOST_PASSWORD` | Email password       | None                       |
| `DEFAULT_FROM_EMAIL`  | Default sender email | None                       |
| `REDIS_URL`           | Redis connection URL | `redis://localhost:6379/0` |
