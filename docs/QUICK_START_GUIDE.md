# Quick Start Guide - nb2prod Web Interface

Welcome to nb2prod! This guide will get you up and running in under 5 minutes.

## Installation

```bash
# Navigate to the project directory
cd nb2prod_working

# Activate virtual environment (if not already active)
source venv/bin/activate

# Install/update dependencies
pip install -e .
```

## Launch the Web Interface

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

## Try It Out with Test Notebooks

We've included two test notebooks to demonstrate all features:

### Option 1: Success Case - `test_notebook.ipynb`

1. **Upload**: Click "Browse files" and select `test_notebook.ipynb`

2. **Analysis Tab**:
   - See production readiness score: **6/10**
   - View detected issues:
     - ⚠️ No functions defined (code organization)
     - ⚠️ Hardcoded file paths detected
   - Check statistics: 24 code cells, 7 imports

3. **Extract Functions Tab**:
   - See **3 extracted functions**:
     - `load_data()` - Data loading and preprocessing
     - `prepare_features()` - Feature engineering
     - `evaluate_model()` - Model evaluation
   - Toggle "Show generated code" to preview functions

4. **Convert to Project Tab**:
   - Click "Generate Project"
   - Download the ZIP file
   - Extract and explore the generated project structure

### Option 2: Error Case - `problematic_notebook.ipynb`

1. **Upload**: Select `problematic_notebook.ipynb`

2. **Analysis Tab**:
   - See production readiness score: **0/10**
   - View critical issues:
     - 🔴 3 execution order problems
     - ⚠️ Hardcoded file paths
   - See detailed cell dependencies showing the problems

3. **Extract/Convert Tabs**:
   - Observe how nb2prod gracefully handles broken notebooks
   - See clear error messages and fix suggestions

## Using AI Enhancement (Optional)

To enable AI-powered code improvement:

1. Get an API key from [Anthropic](https://console.anthropic.com/)

2. In the sidebar:
   - ✅ Check "Enable AI Enhancement"
   - 🔑 Enter your API key

3. Convert a notebook:
   - The AI will improve function names
   - Add comprehensive docstrings
   - Fix parameter handling
   - Create better orchestration

## Command Line Interface

Prefer the terminal? All features are available via CLI:

```bash
# Analyze a notebook
nb2prod analyze test_notebook.ipynb

# See detailed analysis
nb2prod analyze test_notebook.ipynb --detailed

# Extract functions and show code
nb2prod extract test_notebook.ipynb --show-code

# Convert to production project
nb2prod convert test_notebook.ipynb --output ./my_project

# Convert with AI enhancement
export ANTHROPIC_API_KEY="your-key"
nb2prod convert test_notebook.ipynb --enhance --output ./my_project
```

## What Gets Generated?

After conversion, you'll get a complete Python project:

```
my_project/
├── src/
│   ├── __init__.py
│   ├── data_processing.py      # Data loading & cleaning functions
│   ├── feature_engineering.py  # Feature creation functions
│   └── model_training.py       # Model training & evaluation
├── main.py                      # Main execution script
├── config.yaml                  # Configuration file
├── requirements.txt             # All dependencies
└── README.md                    # Project documentation
```

## Running Your Generated Project

```bash
# Navigate to the generated project
cd my_project

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py
```

## Workflow Summary

```
┌─────────────────┐
│  Upload .ipynb  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Analyze (6/10) │  ← Check production readiness
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract (3 fns) │  ← Preview functions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Convert Project │  ← Generate production code
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Download ZIP   │  ← Get your project!
└─────────────────┘
```

## Tips for Best Results

### ✅ Do:
- Use notebooks with sequential workflows (top-to-bottom execution)
- Keep cell execution order correct
- Include all necessary imports at the top
- Use descriptive variable names

### ❌ Avoid:
- Tutorial/educational notebooks with parallel examples
- Notebooks with circular dependencies
- Cells that depend on later cells
- Highly interdependent cells without clear boundaries

## Troubleshooting

**Q: The web interface won't start**
```bash
# Make sure streamlit is installed
pip install streamlit

# Try running directly
python -m streamlit run app.py
```

**Q: "No functions found" error**
- This is normal! nb2prod works best on notebooks without predefined functions
- It extracts logical blocks of code into functions for you

**Q: Generated project doesn't run**
- Check that you have all dependencies installed
- Update file paths in `config.yaml`
- Review the generated `README.md` for specific instructions

**Q: Low production readiness score**
- This shows improvement opportunities
- Review the issues in the Analysis tab
- Fix hardcoded paths and execution order problems

## Next Steps

1. **Try your own notebooks**: Upload a real notebook and see what nb2prod can do
2. **Read the full docs**: Check out [TEST_NOTEBOOKS.md](TEST_NOTEBOOKS.md) for detailed testing guide
3. **Experiment with AI enhancement**: See how Claude AI improves your code
4. **Share feedback**: Report issues or suggest features

## Need Help?

- 📖 Full documentation: [README.md](README.md)
- 🧪 Testing guide: [TEST_NOTEBOOKS.md](TEST_NOTEBOOKS.md)
- 🐛 Report issues: https://github.com/anjan-r-athreya/notebook2production/issues

---

**Enjoy converting your notebooks to production! 🚀**
