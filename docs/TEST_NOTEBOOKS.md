# Test Notebooks for nb2prod

This directory contains test notebooks to thoroughly evaluate all features of nb2prod.

## Available Test Notebooks

### 1. `test_notebook.ipynb` - Production-Ready ML Pipeline

**Purpose**: Test successful conversion and function extraction

**Description**: A realistic customer churn prediction pipeline that demonstrates a typical data science workflow.

**Contents**:
- 24 code cells organized sequentially
- Complete ML pipeline from data loading to evaluation
- Data preprocessing and cleaning
- Feature engineering
- Model training (Random Forest)
- Performance evaluation
- Results saving

**What it Tests**:
- ✅ Successful analysis with moderate score (6/10)
- ✅ Detection of hardcoded paths (`/data/customer_churn.csv`, `/output/`)
- ✅ Detection of missing functions (all code in global scope)
- ✅ Function extraction (should identify 3+ function candidates)
- ✅ Project generation with proper structure
- ✅ AI enhancement capabilities

**Expected Analysis Results**:
```
Production Readiness Score: 6/10
Issues:
- No functions defined (code organization)
- Hardcoded file paths in cells 4, 32, 33
```

**Expected Extracted Functions**:
1. **Data Loading & Preprocessing**: Handles missing values, outlier removal, cleaning
2. **Feature Engineering**: Creates new features, encodes categorical variables
3. **Model Evaluation**: Calculates metrics, generates reports

**Test Commands**:
```bash
# Analyze the notebook
nb2prod analyze test_notebook.ipynb

# See detailed analysis
nb2prod analyze test_notebook.ipynb --detailed

# Extract functions
nb2prod extract test_notebook.ipynb --show-code

# Convert to production project
nb2prod convert test_notebook.ipynb --output ./churn_project

# Convert with AI enhancement
export ANTHROPIC_API_KEY="your-key"
nb2prod convert test_notebook.ipynb --enhance --output ./churn_project_enhanced
```

**Web Interface Testing**:
```bash
streamlit run app.py
# Then upload test_notebook.ipynb and explore all three tabs
```

---

### 2. `problematic_notebook.ipynb` - Error Detection Test

**Purpose**: Test error detection and validation capabilities

**Description**: An intentionally broken notebook with multiple critical issues.

**Contents**:
- 9 code cells with execution order problems
- Variables used before definition
- Multiple hardcoded paths
- Backward dependencies

**What it Tests**:
- ✅ Detection of execution order issues (3 instances)
- ✅ Detection of hardcoded paths (2 locations)
- ✅ Low production readiness score (0/10)
- ✅ Prevention of extraction/conversion (should fail gracefully)
- ✅ Detailed dependency analysis
- ✅ Clear error messages and fix suggestions

**Expected Analysis Results**:
```
Production Readiness Score: 0/10
Issues:
- Cell 2 depends on cell 6 (execution order problem)
- Cell 4 depends on cell 7 (execution order problem)
- Cell 8 depends on cell 9 (execution order problem)
- Hardcoded paths in cells 3, 5
```

**Expected Behavior**:
- **Analyze**: Should detect all 3 execution order issues and hardcoded paths
- **Extract**: Should refuse with message about critical issues
- **Convert**: Should refuse with message about fixing issues first

**Test Commands**:
```bash
# Analyze to see all issues
nb2prod analyze problematic_notebook.ipynb --detailed

# Try to extract (should fail gracefully)
nb2prod extract problematic_notebook.ipynb

# Try to convert (should fail gracefully)
nb2prod convert problematic_notebook.ipynb --output ./test_output
```

---

## Complete Testing Checklist

### CLI Testing

- [ ] **Analysis Command**
  - [ ] Run on `test_notebook.ipynb` (should score 6/10)
  - [ ] Run on `problematic_notebook.ipynb` (should score 0/10)
  - [ ] Test `--detailed` flag for dependency analysis
  - [ ] Verify issue detection (execution order, hardcoded paths, no functions)

- [ ] **Extract Command**
  - [ ] Run on `test_notebook.ipynb` (should find 3 functions)
  - [ ] Test `--show-code` flag
  - [ ] Run on `problematic_notebook.ipynb` (should refuse)
  - [ ] Verify function signatures and categories

- [ ] **Convert Command**
  - [ ] Convert `test_notebook.ipynb` without enhancement
  - [ ] Convert `test_notebook.ipynb` with `--enhance` flag
  - [ ] Verify generated project structure
  - [ ] Test generated code runs successfully
  - [ ] Run on `problematic_notebook.ipynb` (should refuse)

### Web Interface Testing

- [ ] **Upload & Analysis Tab**
  - [ ] Upload `test_notebook.ipynb`
  - [ ] Verify metrics display (cells, functions, imports)
  - [ ] Check production readiness score visualization
  - [ ] Verify issue cards display correctly
  - [ ] Upload `problematic_notebook.ipynb`
  - [ ] Verify critical issues are shown in red

- [ ] **Extract Functions Tab**
  - [ ] View extracted functions from `test_notebook.ipynb`
  - [ ] Toggle "Show generated code" checkbox
  - [ ] Verify function signatures and metadata
  - [ ] Test with `problematic_notebook.ipynb` (should show error)

- [ ] **Convert to Project Tab**
  - [ ] Generate project without AI enhancement
  - [ ] Generate project with AI enhancement (API key required)
  - [ ] Download ZIP file
  - [ ] Extract and verify project structure
  - [ ] Test generated code executes
  - [ ] Verify error handling for problematic notebook

### AI Enhancement Testing (Requires API Key)

- [ ] Set `ANTHROPIC_API_KEY` environment variable
- [ ] Test CLI: `nb2prod convert test_notebook.ipynb --enhance`
- [ ] Test Web UI: Enable AI enhancement toggle
- [ ] Verify enhanced functions have:
  - [ ] Better function names
  - [ ] Comprehensive docstrings
  - [ ] Fixed parameter handling
  - [ ] Improved main.py orchestration

---

## Expected Project Structure

After converting `test_notebook.ipynb`, you should see:

```
output/
├── src/
│   ├── __init__.py
│   ├── data_processing.py    # Data loading and cleaning
│   ├── feature_engineering.py # Feature creation and encoding
│   └── model_evaluation.py    # Model metrics and evaluation
├── main.py                     # Main execution script
├── config.yaml                 # Configuration file
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

## Troubleshooting

### Common Issues

**Issue**: "No code cells found in notebook"
- **Cause**: Empty or corrupted notebook file
- **Fix**: Ensure the .ipynb file is valid JSON

**Issue**: "ANTHROPIC_API_KEY not set"
- **Cause**: API key not configured for enhancement
- **Fix**: `export ANTHROPIC_API_KEY="your-key-here"`

**Issue**: "Notebook has critical execution order issues"
- **Cause**: Cells depend on variables defined later
- **Fix**: Reorder cells or fix dependencies

**Issue**: Generated project doesn't run
- **Cause**: Missing dependencies or data files
- **Fix**: Install requirements.txt and ensure data paths are correct

---

## Creating Your Own Test Notebooks

To create effective test notebooks:

1. **For Success Testing**:
   - Use sequential, logical cell ordering
   - Include realistic data processing workflows
   - Avoid defining functions (let nb2prod extract them)
   - Include some minor issues (hardcoded paths, etc.)

2. **For Error Testing**:
   - Use variables before defining them
   - Add hardcoded absolute paths
   - Create circular dependencies
   - Mix execution order intentionally

3. **Best Practices**:
   - Add markdown cells for context
   - Use realistic variable names
   - Include imports at the top
   - Keep cells focused on single tasks

---

## Next Steps

After testing with these notebooks:

1. Try converting your own real notebooks
2. Report any issues at: https://github.com/anjan-r-athreya/notebook2production/issues
3. Contribute new test cases for edge cases
4. Share successful conversions with the community

---

**Note**: These test notebooks are designed to exercise all features of nb2prod. The `test_notebook.ipynb` represents a realistic success case, while `problematic_notebook.ipynb` demonstrates proper error handling and validation.
