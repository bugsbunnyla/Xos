# Deployment Guide

## Docker (Recommended)
```bash
cd docker
docker-compose up -d
```

## Kubernetes
```bash
kubectl apply -f k8s/
```

## Environment Variables
See `backend/.env.example` for all required variables.

## SSL/TLS
Use Traefik or Nginx as reverse proxy with Let's Encrypt.

## Scaling
- Backend: Horizontal pod autoscaling based on CPU/memory
- DB: Use managed PostgreSQL (RDS, Cloud SQL)
- Search: Elasticsearch cluster with 3+ nodes
- AI: Use OpenAI/Anthropic APIs or deploy Ollama on GPU nodes
