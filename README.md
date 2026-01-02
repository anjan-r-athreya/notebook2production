# nb2prod

Convert messy Jupyter notebooks to production-ready Python code.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Analyze a notebook
nb2prod analyze notebook.ipynb

# Detailed analysis
nb2prod analyze notebook.ipynb --detailed

# Extract function abstraction candidates at a high level
nb2prod extract notebook.ipynb

# Extract function abstraction candidates and show code
nb2prod extract notebook.ipynb --show-code

# Convert to production code (coming soon)
nb2prod convert notebook.ipynb --output ./prod
```

## Features

- AST-based code analysis
- Dependency detection
- Issue identification
- Production readiness scoring
