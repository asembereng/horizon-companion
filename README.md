# 🏗️ Horizon — Companion Code Repository

**Software Development Foundations in the Age of Agentic AI**
*A Practical Guide for the Next Generation of Enterprise Developers*

---

## What is Horizon?

Horizon is a **Team Task & Project Management Platform** built progressively throughout the book. Each chapter adds working code — from a command-line script to a production-ready API with testing, security, CI/CD, and AI agent integration.

The codebase is organized into **three variants** that correspond to the book's parts:

| Variant | Location | Book Parts | Stack |
|---|---|---|---|
| **Classic (stdlib)** | `horizon/core/` | I–V | Python 3.12, stdlib, SQLite, `http.server` |
| **Django / DRF** | `horizon/django/` | VI–VII | Django 5, DRF, PostgreSQL 16, JWT |
| **Enterprise** | `horizon/enterprise/` | VIII | Django + Celery + Redis |

## 📖 Code by Chapter

| Part | Chapter | What Gets Built | Module |
|---|---|---|---|
| I | Ch.3: Programming Fundamentals | CLI task creator | `horizon/core/cli.py` |
| II | Ch.4: Clean Code | Refactored, named, documented | `horizon/core/models.py` |
| II | Ch.5: Design Principles | SOLID-compliant services | `horizon/core/services.py` |
| II | Ch.6: Data Modeling | Database schema + ORM | `horizon/core/database.py` |
| II | Ch.7: APIs | REST API endpoints | `horizon/core/api.py` |
| III | Ch.9: Testing | Full test suite | `tests/` |
| III | Ch.10: Security | Auth, validation, hashing | `horizon/core/auth.py` |
| III | Ch.11: Error Handling | Custom exceptions, logging | `horizon/core/exceptions.py`, `horizon/core/logging_config.py` |
| IV | Ch.12: CI/CD | GitHub Actions pipeline | `.github/workflows/ci.yml` |
| IV | Ch.13: Containers | Dockerfile, docker-compose | `Dockerfile`, `docker-compose.yml` |
| VI | Ch.18: Django Bridge | Django variant setup | `horizon/django/` |
| VI | Ch.22: Architect Agent | Tech stack (Django + DRF + JWT) | `horizon/django/horizon_project/settings.py` |
| VI | Ch.23: Coding Agent | ViewSets, serializers, permissions | `horizon/django/tasks/` |
| VI | Ch.24: QA Agent | pytest-django tests | `horizon/django/tests/` |
| VIII | Ch.25: DevOps Agent | Celery, docker-compose | `horizon/enterprise/`, `docker-compose.yml` |

## 🚀 Quick Start

### Classic (Parts I–V)

```bash
# Clone the repository
git clone https://github.com/Asembereng/horizon-companion.git
cd horizon-companion

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python -m horizon.cli

# Run the tests
pytest -v
```

### Django Variant (Parts VI–VII)

```bash
cd horizon/django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Enterprise Variant (Part VIII)

```bash
# Start the full stack with Docker Compose
docker-compose up --build
```

## 🧪 Running Tests

```bash
# Classic tests (stdlib)
pytest -v --cov=horizon --cov-report=term-missing

# Django tests
cd horizon/django && pytest -v

# Run a specific chapter's tests
pytest tests/test_ch03_cli.py -v
pytest tests/test_ch05_services.py -v
```

## 📂 Project Structure

```
horizon-companion/
├── horizon/
│   ├── __init__.py
│   ├── core/                   # Parts I–V: stdlib variant
│   │   ├── cli.py              # Ch.3: Command-line task creator
│   │   ├── models.py           # Ch.4-5: Domain models (SOLID)
│   │   ├── services.py         # Ch.5: Service layer
│   │   ├── database.py         # Ch.6: Database operations
│   │   ├── api.py              # Ch.7: REST API
│   │   ├── auth.py             # Ch.10: Authentication
│   │   ├── exceptions.py       # Ch.11: Custom exceptions
│   │   └── logging_config.py   # Ch.11: Structured logging
│   ├── django/                 # Parts VI–VII: Django/DRF variant
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── horizon_project/    # Django project settings
│   │   ├── tasks/              # Task app (models, serializers, views)
│   │   ├── users/              # User app
│   │   ├── projects/           # Project app
│   │   └── tests/              # pytest-django tests
│   └── enterprise/             # Part VIII: Enterprise variant
│       ├── celery_app.py       # Celery configuration
│       ├── requirements.txt
│       └── tasks/              # Async Celery tasks
├── tests/                      # Classic test suite
├── Dockerfile                  # Ch.13 (security-hardened)
├── docker-compose.yml          # Ch.25: Full stack
├── .github/
│   ├── workflows/ci.yml        # Ch.12: CI/CD + supply chain scan
│   ├── dependabot.yml          # Ch.10: Dependency updates
│   └── copilot-instructions.md # Ch.23: AI assistant config
├── requirements.txt
└── README.md
```

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
