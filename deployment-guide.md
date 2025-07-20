# Deployment Guide for DormitoriesPlus

## 🐳 Docker Deployment Options

### 1. **Railway** (Recommended for Django + Docker)
Railway is perfect for Django applications with Docker support.

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Railway Configuration:**
- Supports PostgreSQL databases
- Automatic environment variables
- Built-in Redis support
- Easy scaling

### 2. **Render** (Great for Django)
Render provides excellent Django support with Docker.

```bash
# Create render.yaml
services:
  - type: web
    name: dormitoriesplus
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: DEBUG
        value: False
      - key: DB_NAME
        fromDatabase:
          name: dormitoriesplus-db
          property: database
```

### 3. **DigitalOcean App Platform**
Perfect for containerized applications.

```bash
# Deploy via DigitalOcean CLI
doctl apps create --spec app.yaml
```

### 4. **Google Cloud Run**
Serverless containers with auto-scaling.

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/dormitoriesplus
gcloud run deploy dormitoriesplus --image gcr.io/PROJECT_ID/dormitoriesplus
```

### 5. **AWS ECS/Fargate**
Enterprise-grade container orchestration.

```bash
# Deploy with AWS CLI
aws ecs create-service --cluster dormitoriesplus --service-name web
```

## 🚀 Vercel Deployment (Limited)

### Current Vercel Setup
Your current `vercel.json` is configured for serverless deployment, not Docker.

**Limitations with Vercel:**
- ❌ No persistent database connections
- ❌ Limited to serverless functions
- ❌ No background tasks
- ❌ File upload limitations
- ❌ Session storage issues

### Alternative: Vercel + External Database
If you want to use Vercel, you'll need to:
1. Use external database (PlanetScale, Supabase)
2. Convert to serverless functions
3. Use external file storage (AWS S3, Cloudinary)

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up environment variables
- [ ] Configure static file serving
- [ ] Set up email backend
- [ ] Configure CORS settings
- [ ] Set up SSL certificates

### Database Setup
- [ ] PostgreSQL database
- [ ] Redis for caching
- [ ] Database migrations
- [ ] Backup strategy

### Security
- [ ] Strong SECRET_KEY
- [ ] HTTPS enabled
- [ ] Environment variables
- [ ] Database security
- [ ] File upload security

## 🔧 Platform-Specific Configurations

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

## 🌐 Domain and SSL

### Custom Domain Setup
1. Configure DNS records
2. Set up SSL certificates
3. Configure redirects
4. Set up CDN (optional)

### Environment Variables
```bash
# Required for production
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=5432
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Monitoring and Logs

### Health Checks
- Application health endpoint
- Database connectivity
- Redis connectivity
- Static file serving

### Logging
- Application logs
- Error tracking
- Performance monitoring
- Database query monitoring

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: railway/cli@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 💡 Recommendations

### For Production Use:
1. **Railway** - Best for Django + Docker
2. **Render** - Great alternative
3. **DigitalOcean App Platform** - Reliable and scalable
4. **Google Cloud Run** - Serverless containers

### For Development:
1. **Local Docker** - Current setup
2. **Railway** - Easy deployment
3. **Render** - Free tier available

### Avoid for Django:
1. **Vercel** - Limited serverless support
2. **Netlify** - Static site focused
3. **Heroku** - Discontinued free tier 