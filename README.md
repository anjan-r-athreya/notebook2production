# nb2prod

Convert messy Jupyter notebooks to production-ready Python code.

## What It Does

nb2prod analyzes Jupyter notebooks and converts them into clean, production-ready Python projects with:
- Modular functions organized by purpose
- Proper project structure (src/, config, tests)
- CLI entry point
- Documentation and requirements

## Installation

```bash
# Install in development mode
pip install -e .

# Or install dependencies manually
pip install nbformat click rich pyyaml
```

## Commands

### 1. Analyze - Check Notebook Quality

Analyze a notebook for production readiness and identify issues:

```bash
# Basic analysis
nb2prod analyze notebook.ipynb

# Detailed analysis with dependencies
nb2prod analyze notebook.ipynb --detailed
```

**What it checks:**
- ✓ Execution order problems (cells depending on later cells)
- ✓ Hardcoded file paths
- ✓ Code organization (functions vs global scope)
- ✓ Production readiness score (0-10)

**Example output:**
```
Code cells: 12 | Functions: 6 | Imports: 9

Issues Requiring Attention:
  - Cell 5 depends on cell 8 (execution order problem)
  - Found hardcoded paths in cells: 4

Production Readiness Assessment: 6/10
```

### 2. Extract - Preview Function Candidates

Extract and preview function candidates without generating code:

```bash
# Show function candidates
nb2prod extract notebook.ipynb

# Show candidates with generated code
nb2prod extract notebook.ipynb --show-code
```

**What it does:**
- Groups related cells into logical functions
- Detects function parameters and return values
- Suggests function names based on purpose
- Shows which cells would be included

**Example output:**
```
Found 2 function candidate(s):

Function 1: load_data() -> Tuple[pd.DataFrame, pd.Series]
  Category: data
  Source cells: 2, 3, 4
  Returns: X, y
```

### 3. Convert - Generate Production Project

Convert notebook to a complete Python project:

```bash
# Convert to production code
nb2prod convert notebook.ipynb --output ./my_project

# With custom output directory
nb2prod convert notebook.ipynb -o ./prod
```

**Generated structure:**
```
my_project/
├── src/
│   ├── __init__.py
│   ├── data_processing.py      # Data loading/cleaning functions
│   ├── feature_engineering.py  # Feature transformation functions
│   └── model_training.py       # Model training/evaluation functions
├── config.yaml                  # Configuration parameters
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # Usage documentation
```

**Example output:**
```
Converting: notebook.ipynb
Output: ./my_project

Extracted 3 function(s)
Project generated successfully!

Next steps:
  1. cd ./my_project
  2. pip install -r requirements.txt
  3. python main.py
```

## Validation & Safety

nb2prod uses multi-layer validation to ensure quality:

1. **Critical Issues Filter** - Blocks notebooks with execution order problems
2. **Educational Detection** - Identifies tutorial-style notebooks with parallel examples
3. **Hardcoded Paths** - Rejects cells with hardcoded file paths
4. **Forward Dependencies** - Prevents extracting functions that earlier cells depend on
5. **Function Nesting** - Avoids cells containing function definitions
6. **Size Limits** - Maximum 4 cells per function
7. **Dead Code Detection** - Rejects functions with >50% unused variables
8. **I/O Requirements** - Functions must have parameters OR return values

**Philosophy:** "No feedback for the sake of feedback" - only extract production-ready functions.

## Examples

### Example 1: Clean Notebook

```bash
$ nb2prod analyze clean_notebook.ipynb
Code cells: 7 | Functions: 0 | Imports: 4
Production Readiness Assessment: 8/10
Ready for production use with minimal changes.

$ nb2prod convert clean_notebook.ipynb -o ./output
Extracted 1 function(s)
Project generated successfully!
```

### Example 2: Broken Notebook

```bash
$ nb2prod analyze broken_notebook.ipynb
Issues Requiring Attention:
  - Cell 5 depends on cell 6 (execution order problem)
  - 2 cells with hardcoded paths

Production Readiness Assessment: 2/10

$ nb2prod convert broken_notebook.ipynb
Notebook Not Suitable for Conversion
Fix the execution order issues first, then try conversion.
```

### Example 3: Educational Notebook

```bash
$ nb2prod extract tutorial.ipynb
Educational/Tutorial Notebook Detected

This notebook appears to be educational with:
  - 16/28 markdown cells (explanatory content)
  - Repetitive variable patterns (parallel examples)

Function extraction works best on production-style notebooks.
```

## Features

### Phase 1: Analysis ✅
- AST-based code analysis
- Dependency detection (excluding function parameters and loop variables)
- Issue identification with actionable guidance
- Production readiness scoring
- Context-aware warnings (educational notebook detection)

### Phase 2: Function Extraction ✅
- Cell grouping by dependencies and categories
- Function signature generation
- Parameter and return value detection
- Type inference from variable names
- Quality validation (no broken or useless functions)

### Phase 3: Code Generation ✅
- Complete project structure generation
- Organized modules (data, feature, model, visualization)
- CLI entry point with Click
- YAML configuration
- Auto-generated requirements.txt
- Documentation (README.md)

### Phase 4: LLM Enhancement (Planned)
- Smart function naming via Claude API
- Intelligent docstrings
- Code quality improvements
- Test generation

## Project Status

**Current Version:** 0.1.0 (Alpha)

- Phase 1: Analysis - Complete
- Phase 2: Function Extraction - Complete
- Phase 3: Code Generation - Complete
- Phase 4: LLM Enhancement - Planned
- Phase 5: Polish - Planned

## Development

```bash
# Run tests
pytest

# Format code
black .

# Lint
flake8
```

## Architecture

```
nb2prod/
├── parser.py           # Notebook parsing with nbformat
├── simple_analyze.py   # AST-based cell analysis
├── grouper.py         # Cell grouping logic
├── extractor.py       # Function extraction
├── generator.py       # Project generation
└── cli.py             # Click-based CLI
```

## Known Limitations

1. **Minimal main.py output** - Generated main.py prints minimal information
2. **Import detection** - May include unnecessary imports in generated modules
3. **Configuration extraction** - config.yaml is a template, doesn't extract actual config values
4. **Test generation** - Not yet implemented
5. **Partial pipelines** - May extract incomplete workflows if cells don't group well

## Contributing

This is an experimental tool. Feedback and contributions welcome!

## License

MIT
