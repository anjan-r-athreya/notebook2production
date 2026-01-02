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

# Convert to production code (coming soon)
nb2prod convert notebook.ipynb --output ./prod
```

## Features

- AST-based code analysis
- Dependency detection
- Issue identification
- Production readiness scoring
