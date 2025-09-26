# 📝 Todo API — CI/CD Quality Gates Portfolio Project

[![CI/CD Pipeline](https://github.com/Sahar-dev/todo-api-ci-cd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sahar-dev/todo-api-ci-cd/actions)
[![Coverage](https://codecov.io/gh/Sahar-dev/todo-api-ci-cd/branch/master/graph/badge.svg)](https://codecov.io/gh/Sahar-dev/todo-api-ci-cd)
[![Docker Pulls](https://img.shields.io/docker/pulls/sahar-dev/todo-api?label=Docker%20Pulls)](https://hub.docker.com/r/sahar-dev/todo-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Showcase Project for QA & DevOps Engineering:**  
> Modern CI/CD pipeline, automated tests, security gates, and container deployment — engineered for reliability and maintainability.

---
## 🚦 About This Project

This repository demonstrates real-world **QA** and **DevOps** practices through a full-stack Flask Todo API, featuring:

- **Multi-step CI/CD Pipeline:** Built with GitHub Actions — each stage enforces quality, security, and reliability.
- **Automated Testing:** Unit, integration, API, and performance tests.
- **Security at Every Step:** Source code and container vulnerability scanning.
- **Containerization:** Docker & Docker Compose for reproducible environments.
- **Quality Reporting:** Code coverage, performance reports, and pipeline summaries.

Use this repo as a reference for professional **quality engineering** and **DevOps automation**.

---
## 📋 Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for local development)
- k6 (for performance testing)

## 🛡️ CI/CD Quality Gates

The pipeline enforces the following gates (see [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)):

| Gate # | Stage                     | Tool         | Description                     |
|:------:|---------------------------|--------------|---------------------------------|
|   1    | Code Linting              | flake8       | Static style & error checks     |
|   2    | Security Scan (SAST)      | Trivy        | Source vulnerability analysis   |
|   3    | Unit Testing + Coverage   | pytest+cov   | Model/routes logic & coverage   |
|   4    | Docker Image Build        | Dockerfile   | Containerization validation     |
|   5    | Container Security Scan   | docker scan  | Vulnerabilities in image        |
|   6    | API Integration Tests     | curl/pytest  | Endpoint smoke tests            |
|   7    | Performance Tests         | k6           | Load & reliability checks       |
|   8*   | Deployment                | Docker Hub   | Publish image (on master)       |

*Deployment gate runs only on the `master` branch, pushing images to Docker Hub.

---

## 🔬 Automated Testing Strategy

- **Unit Tests:** Flask models and routes
- **API/Integration:** Real API tests (CRUD, edge cases, performance)
- **Performance:** k6 simulates concurrent users, checks latency & success rates
- **Coverage:** Reports uploaded to Codecov

See `tests/unit/` and `tests/api/` for test cases.  
Performance scripts: `tests/performance/k6_test.js`.

---

## 🧑‍💻 Tech Stack & Tools

- **Python:** Flask, SQLAlchemy
- **Testing:** pytest, requests, k6
- **Linting:** flake8
- **Security:** Trivy, docker scan
- **CI/CD:** GitHub Actions
- **Containerization:** Docker, Docker Compose
- **Reporting:** Codecov, workflow summaries

---

## 🏃 Getting Started

### 1. Clone & Build

```bash
git clone https://github.com/Sahar-dev/todo-api-ci-cd.git
cd todo-api-ci-cd
docker-compose up --build
```

API available at `http://localhost:5000`.

### 2. Run Tests

- **Unit tests:**  
  `pytest tests/unit/`
- **API tests:**  
  `pytest tests/api/`
- **Performance:**  
  Requires [k6](https://k6.io/):  
  `k6 run tests/performance/k6_test.js`

---

## 🌐 API Reference

**Base URL:** `http://localhost:5000/api/todos`

| Method | Endpoint                    | Description                |
|--------|-----------------------------|----------------------------|
| GET    | `/api/todos`                | List all todos             |
| POST   | `/api/todos`                | Create new todo            |
| GET    | `/api/todos/<id>`           | Get todo by ID             |
| PUT    | `/api/todos/<id>`           | Update todo                |
| DELETE | `/api/todos/<id>`           | Delete todo                |
| GET    | `/health`                   | Health check               |

---

## 📂 Project Structure

```
app/                # Flask application code
tests/unit/         # Unit tests
tests/api/          # Integration/API tests
tests/performance/  # k6 load tests
Dockerfile          # Container build
docker-compose.yml  # Dev environment
.github/workflows/  # CI/CD pipeline
```

---

## 📊 Reporting & Artifacts

- **Coverage:** [Codecov](https://codecov.io/gh/Sahar-dev/todo-api-ci-cd)
- **Performance:** k6 HTML/JSON reports (workflow artifacts)
- **Pipeline Summaries:** See GitHub Actions run for details

---

## 🏅 Why This Project?

This project is designed as a showcase for:

- **QA Engineering:** Test automation, coverage, reliability
- **DevOps:** End-to-end CI/CD, security gates, containerization, reporting
- **Portfolio:** Demonstrates real-world practices for professional engineering roles

---

## 👤 Author

**Sahar-dev**  
[GitHub](https://github.com/Sahar-dev) | [LinkedIn](https://www.linkedin.com/in/sahar-marzougui/) | [Portfolio](https://sahar-marzougui.netlify.app/)

---

## 📄 License

MIT License

---

## 🤝 Contributing

Issues and PRs are welcome!  
Use this project to learn, improve, and showcase your DevOps & QA skills.

---

## 🌟 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [GitHub Actions](https://github.com/features/actions)
- [k6](https://k6.io/)
- [Trivy](https://github.com/aquasecurity/trivy)
```