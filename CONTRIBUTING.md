# Contributing to nb2prod

Thank you for your interest in contributing to nb2prod! This document provides guidelines and instructions for contributing.

## Getting Started

### Development Setup

1. **Fork and Clone**

```bash
git clone https://github.com/YOUR_USERNAME/notebook2production.git
cd notebook2production
```

2. **Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Development Dependencies**

```bash
pip install -e ".[dev]"
```

This installs:
- pytest (testing)
- pytest-cov (coverage)
- black (formatting)
- flake8 (linting)

### Project Structure

```
nb2prod/
├── cli.py              # CLI interface
├── parser.py           # Notebook parsing
├── simple_analyze.py   # Cell analysis
├── grouper.py          # Cell grouping logic
├── extractor.py        # Function extraction
├── generator.py        # Project generation
├── llm_refactor.py     # AI enhancement
├── tests/              # Test suite
│   ├── conftest.py
│   ├── test_parser.py
│   ├── test_analyzer.py
│   ├── test_generator.py
│   └── test_cli.py
└── setup.py            # Package configuration
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

Follow these guidelines:
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed
- Follow the existing code style

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parser.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### 4. Format Code

```bash
# Format with black
black .

# Check linting
flake8 .
```

### 5. Commit Changes

```bash
git add .
git commit -m "Add feature: brief description"
```

Follow these commit message conventions:
- `Add feature: description` - New features
- `Fix: description` - Bug fixes
- `Update: description` - Updates to existing features
- `Docs: description` - Documentation changes
- `Test: description` - Test additions/changes

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting (line length: 88)
- Use type hints where appropriate
- Write docstrings for all functions/classes

**Example:**

```python
def extract_functions(
    cells: List[Dict[str, Any]],
    threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """Extract functions from notebook cells.

    Args:
        cells: List of code cells from notebook
        threshold: Confidence threshold for extraction

    Returns:
        List of extracted function metadata
    """
    # Implementation
    pass
```

### Testing Guidelines

- Write tests for all new features
- Aim for >80% code coverage
- Use pytest fixtures for common setup
- Test both success and failure cases

**Example:**

```python
def test_parser_handles_invalid_file():
    """Test parser gracefully handles invalid files."""
    with pytest.raises(FileNotFoundError):
        parser = NotebookParser('nonexistent.ipynb')
        parser.parse()
```

## Adding New Features

### Phase-Based Development

nb2prod is organized into phases:

1. **Phase 1**: Parsing and Analysis
2. **Phase 2**: Function Extraction
3. **Phase 3**: Code Generation
4. **Phase 4**: LLM Enhancement
5. **Phase 5**: Polish (tests, docs, packaging)

When adding features, consider which phase they belong to.

### CLI Commands

To add a new CLI command:

1. Add command in `cli.py`:

```python
@cli.command()
@click.argument('notebook', type=click.Path(exists=True))
@click.option('--option', help='Description')
def new_command(notebook, option):
    """Command description."""
    # Implementation
    pass
```

2. Add tests in `tests/test_cli.py`
3. Update README.md documentation

### LLM Integration

When working with LLM features:

- Handle API errors gracefully
- Provide fallback for when API key is missing
- Add timeouts for API calls
- Test with mocked responses

## Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Exact steps to reproduce
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Python version
   - nb2prod version
6. **Sample Notebook**: If possible, attach a minimal notebook that reproduces the issue

## Feature Requests

For feature requests:

1. **Use Case**: Describe the problem you're trying to solve
2. **Proposed Solution**: How you think it should work
3. **Alternatives**: Other approaches you've considered
4. **Examples**: Examples of similar features in other tools

## Code Review Process

All contributions require review before merging:

1. Automated tests must pass
2. Code coverage should not decrease
3. Code must follow style guidelines
4. Documentation must be updated
5. At least one maintainer approval required

## Questions?

- Open an issue for questions
- Tag with `question` label
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes
- README credits section

Thank you for contributing to nb2prod!
