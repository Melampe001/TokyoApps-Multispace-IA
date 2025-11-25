# Self-Hosted Runners for Tokyo IA

Este directorio contiene configuraciones para ejecutar runners auto-hospedados.

## 🐍 Python Runner

Runner optimizado para proyectos Python.

### Características:
- Python 3.9, 3.10, 3.11, 3.12 pre-instalados
- pip, poetry, pipenv disponibles
- Herramientas de linting: black, flake8, pylint, mypy
- Testing: pytest, pytest-cov
- Docker pre-instalado

### Uso:
```bash
docker build -t tokyo-ia-runner:python -f Dockerfile.python .
docker run -d --name tokyo-runner-python tokyo-ia-runner:python
```

## 🐳 Docker Runner

Runner con Docker-in-Docker para builds de contenedores.

### Características:
- Docker y Docker Compose
- Buildx para multi-arch builds
- Registry cache

### Uso:
```bash
docker build -t tokyo-ia-runner:docker -f Dockerfile.docker .
docker run -d --privileged --name tokyo-runner-docker tokyo-ia-runner:docker
```

## 📈 Autoscale Runner

Configuración para runners auto-escalables con Kubernetes.

### Características:
- Escalado automático basado en jobs
- Múltiples réplicas
- Limpieza automática

### Requisitos:
- Cluster Kubernetes
- Helm 3.x
- Actions Runner Controller

### Uso:
```bash
helm install arc oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
kubectl apply -f runner-deployment.yaml
```

## 🔧 Configuración

### Variables de entorno requeridas:
- `GITHUB_TOKEN`: Token de acceso personal o App token
- `GITHUB_OWNER`: Propietario del repositorio
- `GITHUB_REPO`: Nombre del repositorio

### Registro de runner:
```bash
./config.sh --url https://github.com/OWNER/REPO --token YOUR_TOKEN
```

## 📊 Monitoreo

Los runners reportan métricas a través de:
- Prometheus (puerto 9090)
- Logs estructurados en JSON

## 🛡️ Seguridad

- Runners ejecutan en contenedores aislados
- Secrets nunca se persisten en disco
- Limpieza automática después de cada job
