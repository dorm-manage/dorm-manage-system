# Platform-Specific Configurations

### Railway

```yaml
# railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT DormitoriesPlus_project.wsgi:application",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: dormitoriesplus
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: DEBUG
        value: False
      - key: PORT
        value: 8000
    healthCheckPath: /
    autoDeploy: true
```

### DigitalOcean

```yaml
# app.yaml
name: dormitoriesplus
services:
  - name: web
    source_dir: /
    dockerfile_path: Dockerfile
    http_port: 8000
    routes:
      - path: /
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
```
