#!/bin/bash

# Railway deployment script for DormitoriesPlus
set -e

echo "🚂 Deploying to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed. Installing..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

# Initialize Railway project if not already done
if [ ! -f "railway.json" ]; then
    echo "📝 Creating Railway configuration..."
    cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:\$PORT DormitoriesPlus_project.wsgi:application",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "numReplicas": 1
  }
}
EOF
fi

# Deploy to Railway
echo "🚀 Deploying application..."
railway up

echo "✅ Deployment completed!"
echo "🌐 Your application is now live on Railway!"
echo "📊 Check your Railway dashboard for the URL" 