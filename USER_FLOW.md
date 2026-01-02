Persona: Sarah (Data Scientist)
Current pain:

Has a notebook: customer_churn_model.ipynb (300 lines, messy)
Works on her laptop
ML engineer keeps asking her to "clean it up for production"
She doesn't know how / doesn't have time

Her flow with nb2prod:

The Complete User Experience
Step 1: Installation
Terminal:
bashpip install nb2prod
```

**Output:**
```
✓ Installing nb2prod...
✓ Dependencies installed
✓ Ready to use!

Try: nb2prod convert your_notebook.ipynb

Step 2: First Run (Discovery)
Sarah navigates to her notebook directory:
bashcd ~/projects/churn-analysis/
nb2prod convert customer_churn_model.ipynb
```

**What she sees (colorful terminal output):**
```
🔍 Analyzing notebook: customer_churn_model.ipynb

📊 Notebook Structure:
   ├─ 47 code cells
   ├─ 12 markdown cells  
   ├─ 8 imports detected
   └─ 23 variables defined

⚠️  Issues Found:
   • Cells 5, 12, 28 have execution order dependencies
   • 6 hardcoded file paths detected
   • No functions defined (all global scope)
   • 3 cells with unused variables

🎯 Production Readiness Score: 3/10

Would you like to:
  [1] See detailed analysis
  [2] Auto-convert to production code
  [3] Exit

Choice: 
```

Sarah types `1` (detailed analysis):
```
📋 Detailed Analysis:

EXECUTION ORDER ISSUES:
  ⚠️  Cell 12 uses 'processed_df' from Cell 5
      But also uses 'scaler' from Cell 28
      Risk: Non-linear execution dependencies

HARDCODED VALUES:
  📁 Cell 3: data_path = "/Users/sarah/data/customers.csv"
  📁 Cell 8: model_path = "./models/best_model.pkl"
  🔢 Cell 15: epochs = 100
  🔢 Cell 15: learning_rate = 0.001
  🔢 Cell 20: test_size = 0.2

SUGGESTED FUNCTIONS:
  📦 Cells 3-7: Data loading & cleaning
     → Suggest: load_and_clean_data(path: str) -> DataFrame
  
  📦 Cells 8-14: Feature engineering  
     → Suggest: engineer_features(df: DataFrame) -> DataFrame
  
  📦 Cells 15-25: Model training
     → Suggest: train_model(X, y, epochs, lr) -> Model

💡 Ready to auto-convert? (y/n):

Step 3: Conversion (The Magic)
Sarah types y:
bashnb2prod convert customer_churn_model.ipynb --output ./production_code
```

**Live output with progress:**
```
🚀 Converting to production code...

[████████░░] 80% Analyzing dependencies...
[██████████] 100% ✓ Dependency graph built

🤖 Using AI to improve code structure...
[████████░░] 80% Suggesting function boundaries...
[██████████] 100% ✓ Generated 5 functions

📝 Generating code files...
  ✓ src/data.py (3 functions, 87 lines)
  ✓ src/features.py (2 functions, 64 lines)
  ✓ src/model.py (4 functions, 156 lines)
  ✓ src/config.py (configuration extracted)
  ✓ main.py (CLI entry point)
  ✓ requirements.txt (8 packages)
  ✓ tests/test_data.py (5 tests)

📦 Generated in: ./production_code/

🎉 Conversion complete!

Next steps:
  cd production_code
  python main.py --help

Step 4: Exploring the Output
Sarah runs:
bashcd production_code
tree
```

**What she sees:**
```
production_code/
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── features.py
│   ├── model.py
│   └── config.py
├── tests/
│   ├── test_data.py
│   └── test_features.py
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
└── .conversion_report.md
She opens src/data.py:
python"""
Data loading and preprocessing functions.

Auto-generated from customer_churn_model.ipynb
Original cells: 3-7
"""

import pandas as pd
from pathlib import Path
from typing import Optional

def load_raw_data(data_path: str) -> pd.DataFrame:
    """
    Load customer data from CSV.
    
    Args:
        data_path: Path to customer CSV file
        
    Returns:
        Raw customer dataframe
        
    Raises:
        FileNotFoundError: If data file doesn't exist
    """
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw customer data.
    
    Args:
        df: Raw dataframe
        
    Returns:
        Cleaned dataframe with:
        - Removed null values
        - Standardized column names  
        - Type conversions applied
    """
    # Remove nulls (from cell 4)
    df = df.dropna()
    
    # Standardize columns (from cell 5)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Convert types (from cell 6)
    df['customer_id'] = df['customer_id'].astype(str)
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    
    return df


def load_and_clean_data(data_path: str) -> pd.DataFrame:
    """
    Complete data loading pipeline.
    
    Args:
        data_path: Path to customer CSV
        
    Returns:
        Cleaned, ready-to-use dataframe
    """
    df = load_raw_data(data_path)
    df = clean_data(df)
    return df
Comments in the code show:

Which notebook cells became this function
Docstrings explain what it does
Type hints added
Error handling added


Step 5: The Config File
She opens config.yaml:
yaml# Auto-extracted from customer_churn_model.ipynb
# Original hardcoded values are now configurable

data:
  input_path: "/Users/sarah/data/customers.csv"
  output_path: "./models/best_model.pkl"

model:
  epochs: 100
  learning_rate: 0.001
  batch_size: 32

evaluation:
  test_size: 0.2
  random_state: 42
She thinks: "Oh wow, I can now change these without touching code!"

Step 6: The CLI
bashpython main.py --help
```

**Output:**
```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Customer Churn Prediction Pipeline
  Auto-generated from customer_churn_model.ipynb

Options:
  --config PATH  Path to config file [default: config.yaml]
  --verbose      Enable detailed logging
  --help         Show this message

Commands:
  train     Train the churn prediction model
  predict   Make predictions on new data  
  evaluate  Evaluate model performance
Running it:
bashpython main.py train --data ./data/customers.csv
```

**Output:**
```
🚂 Training churn prediction model...

✓ Loading data from ./data/customers.csv
  → Loaded 10,000 rows

✓ Cleaning data
  → Removed 142 null rows
  → 9,858 rows remaining

✓ Engineering features
  → Created 12 new features

✓ Training model
  Epoch 1/100 - Loss: 0.4521
  Epoch 50/100 - Loss: 0.2103
  Epoch 100/100 - Loss: 0.1847

✓ Model trained successfully
  → Saved to ./models/best_model.pkl

📊 Training Summary:
  Accuracy: 87.3%
  F1 Score: 0.812
  Training time: 2m 34s

Step 7: The Tests
Sarah runs:
bashpytest tests/
```

**Output:**
```
======================== test session starts =========================
collected 12 items

tests/test_data.py ......                                      [ 50%]
tests/test_features.py ....                                    [ 83%]
tests/test_model.py ..                                         [100%]

======================== 12 passed in 3.45s =========================
She opens tests/test_data.py:
python"""
Tests for data loading and cleaning.
Auto-generated from notebook execution.
"""

import pytest
import pandas as pd
from src.data import load_raw_data, clean_data


@pytest.fixture
def sample_data():
    """Sample customer data matching notebook format."""
    return pd.DataFrame({
        'Customer ID': ['C001', 'C002', 'C003'],
        'Signup Date': ['2023-01-01', '2023-02-15', None],
        'Monthly Charge': [50.0, 75.5, 100.0]
    })


def test_clean_data_removes_nulls(sample_data):
    """Test that null rows are removed."""
    result = clean_data(sample_data)
    assert len(result) == 2
    assert result.isna().sum().sum() == 0


def test_clean_data_standardizes_columns(sample_data):
    """Test that column names are standardized."""
    result = clean_data(sample_data.dropna())
    assert 'customer_id' in result.columns
    assert 'signup_date' in result.columns
    assert 'Customer ID' not in result.columns

Step 8: The Report
Sarah opens .conversion_report.md:
markdown# Conversion Report: customer_churn_model.ipynb

**Converted on:** 2024-12-30 14:23:45
**Production Readiness:** 3/10 → 8/10

## What Was Changed

### ✅ Improvements Made
- Extracted 9 functions from 47 cells
- Moved 6 hardcoded values to config.yaml
- Added type hints to all functions
- Generated 12 unit tests
- Created CLI interface
- Added error handling

### 📊 Code Structure
**Before:**
- 1 file (notebook)
- 0 functions
- 0 tests
- Global scope only

**After:**
- 7 Python files
- 9 functions with docs
- 12 tests (100% pass rate)
- Modular structure

### 🔧 Manual Review Needed

⚠️ **Cell 28-30**: Complex sklearn pipeline
   - Auto-conversion was conservative
   - Consider refactoring for better clarity
   - See src/model.py lines 78-103

⚠️ **Cell 42**: Matplotlib visualization
   - Moved to separate utility
   - May want to integrate with reporting

### 📝 Next Steps

1. **Review generated code** - especially flagged sections
2. **Test with real data** - run `python main.py train`
3. **Adjust config.yaml** - update paths for your environment
4. **Add more tests** - for edge cases
5. **Share with engineering** - they can review src/ files

## Files Generated

| File | Lines | Purpose |
|------|-------|---------|
| src/data.py | 87 | Data loading & cleaning |
| src/features.py | 64 | Feature engineering |
| src/model.py | 156 | Model training & eval |
| src/config.py | 23 | Config management |
| main.py | 112 | CLI entry point |
| tests/test_*.py | 98 | Unit tests |

## Cell Mapping

See detailed mapping in `.cell_mapping.json`

