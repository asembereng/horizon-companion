# Horizon project conventions
# Chapter 23 (Coding Agent): Project-level instructions for AI assistants

## Language and runtime
- Python 3.11+, stdlib only (no third-party packages unless listed below)
- Approved packages: bcrypt, PyJWT, pytest

## Code style
- Type annotations on all public functions
- Docstrings: one-line summary then blank line then detail
- Snake_case for functions and variables; PascalCase for classes

## Testing
- Every new function must have a corresponding test in tests/
- Use pytest fixtures; never share mutable state between tests

## Security
- Never hardcode secrets; read from os.environ
- Hash passwords with bcrypt.hashpw(pwd, bcrypt.gensalt(rounds=12))
