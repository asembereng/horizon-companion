# 🏗️ Horizon — Companion Code Repository

**Software Development Foundations in the Age of Agentic AI**
*A Practical Guide for the Next Generation of Enterprise Developers*

---

## What is Horizon?

Horizon is a **Team Task & Project Management Platform** built progressively throughout the book. Each chapter adds working code — from a command-line script to a production-ready API with testing, security, CI/CD, and AI agent integration.

## 📖 Code by Chapter

| Part | Chapter | What Gets Built | Module |
|---|---|---|---|
| I | Ch.3: Programming Fundamentals | CLI task creator | `horizon/cli.py` |
| II | Ch.4: Clean Code | Refactored, named, documented | `horizon/models.py` |
| II | Ch.5: Design Principles | SOLID-compliant services | `horizon/services.py` |
| II | Ch.6: Data Modeling | Database schema + ORM | `horizon/database.py` |
| II | Ch.7: APIs | REST API endpoints | `horizon/api.py` |
| III | Ch.9: Testing | Full test suite | `tests/` |
| III | Ch.10: Security | Auth, validation, hashing | `horizon/auth.py` |
| III | Ch.11: Error Handling | Custom exceptions, logging | `horizon/exceptions.py`, `horizon/logging_config.py` |
| IV | Ch.12: CI/CD | GitHub Actions pipeline | `.github/workflows/ci.yml` |
| IV | Ch.13: Containers | Dockerfile | `Dockerfile` |

## 🚀 Quick Start

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

## 📚 Documentation

Visit the [Horizon Code Companion](https://asembereng.github.io/horizon-companion/) for detailed explanations of every code snippet in the book.

## 🧪 Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=horizon --cov-report=term-missing

# Run a specific chapter's tests
pytest tests/test_ch03_cli.py -v
pytest tests/test_ch05_services.py -v
```

## 📂 Project Structure

```
horizon-companion/
├── horizon/                # Application code
│   ├── __init__.py
│   ├── cli.py             # Ch.3: Command-line task creator
│   ├── models.py          # Ch.4-5: Domain models (SOLID)
│   ├── services.py        # Ch.5: Service layer
│   ├── database.py        # Ch.6: Database operations
│   ├── api.py             # Ch.7: REST API
│   ├── auth.py            # Ch.10: Authentication
│   ├── exceptions.py      # Ch.11: Custom exceptions
│   └── logging_config.py  # Ch.11: Structured logging
├── tests/                  # Test suite
│   ├── test_ch03_cli.py
│   ├── test_ch04_models.py
│   ├── test_ch05_services.py
│   ├── test_ch06_database.py
│   ├── test_ch07_api.py
│   ├── test_ch09_testing.py
│   ├── test_ch10_security.py
│   └── test_ch11_errors.py
├── docs/                   # GitHub Pages site
├── Dockerfile             # Ch.13
├── .github/workflows/     # Ch.12: CI/CD
├── requirements.txt
└── README.md
```

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
