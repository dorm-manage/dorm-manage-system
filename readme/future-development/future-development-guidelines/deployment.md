# Deployment

#### Supported Platforms

* **Railway**: `railway.json`
* **Render**: `render.yaml`
* **Vercel**: `vercel.json`
* **Docker**: Production-ready containers

#### Database Configuration

The system uses **PostgreSQL** hosted on **Supabase** for production. Database configuration is managed through environment variables.

**Environment Variables**

see ".evn" file

#### Deployment Scripts

```bash
# Railway deployment
./scripts/deploy-railway.sh

# Docker setup
./scripts/docker-setup.sh
```
