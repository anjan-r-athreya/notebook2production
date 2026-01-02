# nb2prod - Product Specification

## What We're Building
A CLI tool that converts messy Jupyter notebooks into production-ready Python code.

## Target User
Data scientists who have working notebooks but need them productionized.

## Core User Flow

### Input
- Messy Jupyter notebook with:
  - Cells in any order
  - Hardcoded paths/values
  - No functions, all global scope
  - No tests

### Output
- Clean Python project:
  - src/ with modular functions
  - config.yaml with extracted values
  - tests/ with generated tests
  - main.py with CLI
  - Full documentation

### Commands
1. `nb2prod analyze notebook.ipynb` - Shows issues
2. `nb2prod convert notebook.ipynb --output ./prod` - Converts

## Success Criteria
- Engineer can review generated code without complaints
- Code passes basic pytest
- Takes <5 minutes to convert a notebook
- 80% of generated code needs no manual edits

## Technical Constraints
- Pure Python, no web UI
- Works offline (except LLM calls)
- Handles notebooks up to 100 cells
- Dependencies: nbformat, click, rich, anthropic
```
