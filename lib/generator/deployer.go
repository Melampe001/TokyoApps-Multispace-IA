// Package generator provides deployment configuration generation.
package generator

import (
	"fmt"
)

// Deployer handles generation of deployment configurations.
type Deployer struct{}

// NewDeployer creates a new Deployer instance.
func NewDeployer() *Deployer {
	return &Deployer{}
}

// GenerateDockerCompose creates a docker-compose.yml file.
func (d *Deployer) GenerateDockerCompose(config *ProjectConfig) (string, error) {
	var compose string

	switch config.Type {
	case ProjectTypeAPI:
		compose = `version: '3.8'

services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
`

	case ProjectTypeEcommerce:
		compose = `version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
`

	case ProjectTypeBot, ProjectTypeAIAgent:
		compose = `version: '3.8'

services:
  bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - API_KEY=${API_KEY}
    restart: unless-stopped
`

	case ProjectTypePWA:
		compose = `version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
`
	}

	return compose, nil
}

// GenerateKubernetesManifest creates basic Kubernetes deployment manifests.
func (d *Deployer) GenerateKubernetesManifest(config *ProjectConfig) (string, error) {
	manifest := fmt.Sprintf(`apiVersion: apps/v1
kind: Deployment
metadata:
  name: %s
  labels:
    app: %s
spec:
  replicas: 3
  selector:
    matchLabels:
      app: %s
  template:
    metadata:
      labels:
        app: %s
    spec:
      containers:
      - name: %s
        image: %s:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENV
          value: "production"
---
apiVersion: v1
kind: Service
metadata:
  name: %s
spec:
  selector:
    app: %s
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
`, config.Name, config.Name, config.Name, config.Name, config.Name, config.Name, config.Name, config.Name)

	return manifest, nil
}

// GenerateDeploymentREADME creates deployment documentation.
func (d *Deployer) GenerateDeploymentREADME(config *ProjectConfig) (string, error) {
	doc := fmt.Sprintf(`# Deployment Guide for %s

## Docker Deployment

### Build and Run with Docker

`+"```bash"+`
docker build -t %s .
docker run -p 8080:8080 %s
`+"```"+`

### Using Docker Compose

`+"```bash"+`
docker-compose up -d
`+"```"+`

## Kubernetes Deployment

### Prerequisites

- kubectl configured
- Access to a Kubernetes cluster

### Deploy

`+"```bash"+`
kubectl apply -f deploy/kubernetes.yaml
`+"```"+`

### Check Status

`+"```bash"+`
kubectl get pods
kubectl get services
`+"```"+`

## Cloud Platforms

### Vercel (for PWAs and Next.js)

1. Install Vercel CLI: `+"`npm i -g vercel`"+`
2. Run: `+"`vercel`"+`
3. Follow the prompts

### Heroku

1. Install Heroku CLI
2. Login: `+"`heroku login`"+`
3. Create app: `+"`heroku create`"+`
4. Deploy: `+"`git push heroku main`"+`

### AWS

See [aws-deploy.md](aws-deploy.md) for detailed AWS deployment instructions.

### Google Cloud Platform

See [gcp-deploy.md](gcp-deploy.md) for detailed GCP deployment instructions.

## Environment Variables

Make sure to set the following environment variables:

`, config.Name, config.Name, config.Name)

	// Add environment variables based on project type
	switch config.Type {
	case ProjectTypeAPI, ProjectTypeEcommerce:
		doc += `- ` + "`DATABASE_URL`" + ` - Database connection string
`
	}

	if config.Type == ProjectTypeEcommerce {
		doc += `- ` + "`STRIPE_SECRET_KEY`" + ` - Stripe API key
- ` + "`STRIPE_WEBHOOK_SECRET`" + ` - Stripe webhook secret
`
	}

	if config.Type == ProjectTypeBot || config.Type == ProjectTypeAIAgent {
		doc += `- ` + "`BOT_TOKEN`" + ` - Bot authentication token
- ` + "`API_KEY`" + ` - API key for external services
`
	}

	doc += `
## Monitoring

- Setup health check endpoint: ` + "`/health`" + `
- Configure logging
- Setup error tracking (e.g., Sentry)

## Scaling

### Horizontal Scaling

` + "```bash" + `
kubectl scale deployment %s --replicas=5
` + "```" + `

### Auto-scaling

` + "```bash" + `
kubectl autoscale deployment %s --cpu-percent=80 --min=3 --max=10
` + "```" + `
`

	doc = fmt.Sprintf(doc, config.Name, config.Name)

	return doc, nil
}
