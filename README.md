# Todo API CI/CD Pipeline Project

A demonstration of modern CI/CD practices with quality gates for a Flask Todo API.

## 🚀 Features

- **7 Quality Gates** ensuring code quality at every stage
- **Automated Testing** (Unit + API + Smoke tests)
- **Security Scanning** (SAST + Container vulnerability scanning)
- **Dockerized Application**
- **GitHub Actions Pipeline**

## 📋 Quality Gates

1. **Code Linting** (flake8)
2. **Security Scanning** (Trivy SAST)
3. **Unit Tests with Coverage** (pytest)
4. **Docker Image Build**
5. **Container Security Scan**
6. **API Integration Tests**
7. **Production Smoke Tests**

## 🛠️ Tech Stack

- Python Flask
- pytest
- Docker
- GitHub Actions
- Trivy (Security)
- flake8 (Linting)

## 🏃‍♂️ Running Locally

```bash
# Clone repository
git clone <your-repo>
cd todo-api-ci-cd

# Run with Docker
docker-compose up --build

# Run tests
pytest tests/unit/
pytest tests/api/