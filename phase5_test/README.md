# Generated Project

This project was automatically generated from a Jupyter notebook using nb2prod.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --config config.yaml
```

## Project Structure

- `src/` - Source code modules
- `config.yaml` - Configuration parameters
- `main.py` - Main CLI entry point
- `requirements.txt` - Python dependencies

## Generated Functions

### `load_data`

Category: data
Returns: X, df, feature_columns, y

### `engineer_features`

Category: feature
Returns: X_test, model, y_test, y_test_pred, y_test_proba, y_train, y_train_pred

### `train_model`

Category: model
Returns: test_precision, test_recall

### `engineer_features`

Category: feature
Parameters: customer, idx
