# Deployment Guide

## Prerequisites

- Docker installed
- Firebase project configured
- GitHub account
- Heroku account (optional)
- AWS/GCP/Azure account (optional)

## Environment Variables

Create `.env` file with:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-min-32-chars
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_DATABASE_URL=your-database-url
FIREBASE_STORAGE_BUCKET=your-storage-bucket
CORS_ORIGINS=https://yourdomain.com
```

## Local Docker Deployment

```bash
# Build image
docker build -t lifeline-ai:latest .

# Run container
docker run -p 5000:5000 --env-file .env lifeline-ai:latest

# Or with docker-compose
docker-compose up -d
```

## Heroku Deployment

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FIREBASE_PROJECT_ID=your-project-id
heroku config:set FIREBASE_PRIVATE_KEY=your-private-key
heroku config:set FIREBASE_CLIENT_EMAIL=your-client-email
heroku config:set FIREBASE_DATABASE_URL=your-database-url
heroku config:set FIREBASE_STORAGE_BUCKET=your-storage-bucket

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 lifeline-ai

# Create environment
eb create lifeline-ai-env

# Set environment variables
eb setenv FLASK_ENV=production SECRET_KEY=your-secret-key ...

# Deploy
eb deploy

# Monitor
eb open
```

## GCP Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/your-project/lifeline-ai

# Deploy
gcloud run deploy lifeline-ai \
  --image gcr.io/your-project/lifeline-ai \
  --platform managed \
  --region us-central1 \
  --set-env-vars FLASK_ENV=production,FIREBASE_PROJECT_ID=... \
  --allow-unauthenticated
```

## Azure App Service

```bash
# Create resource group
az group create --name lifeline-ai --location eastus

# Create app service plan
az appservice plan create --name lifeline-ai-plan \
  --resource-group lifeline-ai --sku B1 --is-linux

# Create web app
az webapp create --resource-group lifeline-ai \
  --plan lifeline-ai-plan --name lifeline-ai \
  --runtime "python|3.10"

# Deploy
az webapp up --resource-group lifeline-ai --name lifeline-ai
```

## CI/CD with GitHub Actions

The repository includes `.github/workflows/ci-cd.yml` that:

1. Runs tests on every push
2. Builds Docker image
3. Uploads coverage reports

## Monitoring & Logging

### Health Check
```bash
curl http://your-domain/api/health
```

### Logs

With Docker:
```bash
docker logs <container-id>
```

With Heroku:
```bash
heroku logs --tail
```

## Scaling

### Docker Swarm
```bash
docker swarm init
docker service create --replicas 3 -p 5000:5000 lifeline-ai:latest
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
kubectl scale deployment lifeline-ai --replicas=3
```

## SSL/TLS Certificate

### Let's Encrypt with Nginx
```bash
certbot certonly --nginx -d yourdomain.com
```

### AWS Certificate Manager
- Request certificate in ACM
- Validate domain
- Attach to ALB
