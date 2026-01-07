# nb2prod

Convert messy Jupyter notebooks to production-ready Python code using AI-powered analysis and refactoring.

## Features

- **Smart Analysis**: Detect production readiness issues, execution order problems, and code quality concerns
- **Function Extraction**: Automatically identify and extract reusable functions from notebook cells
- **AI Enhancement**: Use Claude AI to improve function names, add docstrings, and fix dependencies
- **Project Generation**: Create complete Python projects with proper structure, tests, and configuration
- **Educational Notebook Detection**: Identifies tutorial/educational notebooks vs production workflows

## Installation

```bash
# Clone the repository
git clone https://github.com/anjan-r-athreya/notebook2production.git
cd notebook2production

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package
pip install -e .

# For development (includes pytest, black, flake8)
pip install -e ".[dev]"
```

## Quick Start

### Web Interface (Recommended)

Launch the web interface for an easy-to-use graphical experience:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` and:
1. Upload your .ipynb file
2. View analysis results and production readiness score
3. Extract and preview functions
4. Convert to a production project (with optional AI enhancement)
5. Download the generated project as a ZIP file

### Command Line Interface

### 1. Analyze a Notebook

```bash
nb2prod analyze your_notebook.ipynb
```

This will show:
- Production readiness score (0-10)
- Execution order issues
- Hardcoded paths
- Missing function organization

### 2. Extract Functions

```bash
nb2prod extract your_notebook.ipynb --show-code
```

Identifies logical function candidates and shows generated code.

### 3. Convert to Production Project

```bash
# Basic conversion
nb2prod convert your_notebook.ipynb --output ./my_project

# With AI enhancement (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY="your-api-key"
nb2prod convert your_notebook.ipynb --enhance --output ./my_project
```

This creates a complete project with:
```
my_project/
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── feature_engineering.py
│   └── model_training.py
├── main.py
├── config.yaml
├── requirements.txt
└── README.md
```

## Commands

### `analyze`

Analyze notebook for production readiness issues.

```bash
nb2prod analyze NOTEBOOK [--detailed]
```

**Options:**
- `--detailed`: Show detailed cell-by-cell dependency analysis

### `extract`

Extract function suggestions from notebook.

```bash
nb2prod extract NOTEBOOK [--show-code]
```

**Options:**
- `--show-code`: Display the generated function code

### `convert`

Convert notebook to production-ready Python project.

```bash
nb2prod convert NOTEBOOK [--output DIR] [--enhance]
```

**Options:**
- `--output, -o DIR`: Output directory (default: `./output`)
- `--enhance`: Use Claude AI to enhance functions (requires `ANTHROPIC_API_KEY`)

## AI Enhancement

The `--enhance` flag uses Claude AI to:
- Generate better function names
- Add comprehensive docstrings
- Fix missing parameters
- Improve return value handling
- Fix cross-function dependencies
- Create an intelligent main.py with proper orchestration

**Setup:**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
nb2prod convert notebook.ipynb --enhance
```

## Testing nb2prod

We provide comprehensive test notebooks to help you explore all features:

### Test Notebooks

1. **`test_notebook.ipynb`** - Production ML Pipeline
   - Realistic customer churn prediction workflow
   - Tests successful analysis, extraction, and conversion
   - Expected score: 6/10 (demonstrates typical improvement opportunities)

2. **`problematic_notebook.ipynb`** - Error Detection
   - Intentionally broken notebook with execution order issues
   - Tests error detection and validation
   - Expected score: 0/10 (demonstrates issue identification)

### Quick Test

```bash
# Test analysis
nb2prod analyze test_notebook.ipynb

# Test function extraction
nb2prod extract test_notebook.ipynb --show-code

# Test web interface
streamlit run app.py
# Then upload test_notebook.ipynb
```

See [TEST_NOTEBOOKS.md](TEST_NOTEBOOKS.md) for complete testing guide and checklist.

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

### Code Formatting

```bash
black .
flake8 .
```

## Architecture

nb2prod uses a multi-phase approach:

1. **Phase 1: Foundation** - Notebook parsing and AST analysis
2. **Phase 2: Function Extraction** - Cell grouping and function identification
3. **Phase 3: Code Generation** - Project structure creation
4. **Phase 4: LLM Enhancement** - AI-powered code improvement
5. **Phase 5: Polish** - Tests, docs, and packaging

## Examples

### Example 1: Data Science Workflow

```bash
# Analyze a machine learning notebook
nb2prod analyze ml_model.ipynb --detailed

# Extract functions with AI enhancement
export ANTHROPIC_API_KEY="sk-..."
nb2prod convert ml_model.ipynb --enhance --output ./ml_project

# Run the generated project
cd ml_project
pip install -r requirements.txt
python main.py
```

### Example 2: Quick Refactoring

```bash
# Just see what functions can be extracted
nb2prod extract data_analysis.ipynb --show-code

# Convert without AI (faster, free)
nb2prod convert data_analysis.ipynb --output ./refactored
```

## Configuration

Generated projects include a `config.yaml` file for easy parameter management:

```yaml
pipeline:
  name: 'My Data Pipeline'
  version: '1.0.0'

data:
  random_state: 42
  test_size: 0.2

output:
  save_results: true
  results_dir: 'results'
```

## Limitations

- **Educational Notebooks**: nb2prod works best on production-style notebooks with sequential workflows. Tutorial notebooks with parallel examples may not convert well.
- **Execution Order**: Notebooks must have correct execution order (top-to-bottom).
- **Complex Dependencies**: Highly interdependent cells may require manual adjustment.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Built with:
- [nbformat](https://github.com/jupyter/nbformat) - Jupyter notebook format
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Anthropic Claude](https://www.anthropic.com/) - AI enhancement

## Support

- **Issues**: https://github.com/anjan-r-athreya/notebook2production/issues
- **Documentation**: See `mdfiles/` directory for detailed specs

## Roadmap

- [ ] Add support for R notebooks
- [ ] Generate unit tests automatically
- [ ] Support for Streamlit app generation
- [ ] Integration with CI/CD pipelines
- [ ] VS Code extension
