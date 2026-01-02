"""Functions for data operations."""

from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np

def load_data() -> Tuple[Any, Any, np.ndarray, np.ndarray]:
    """Load and preprocess data.
    
    Returns:
        Tuple containing:
        - LogisticRegression
        - StandardScaler
        - X
        - y
    """
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression

    # Create sample data (no hardcoded paths)
    data = {
        'age': [25, 30, 35, 40, 45, 50],
        'income': [50000, 60000, 70000, 80000, 90000, 100000],
        'target': [0, 0, 1, 1, 1, 1]
    }
    df = pd.DataFrame(data)

    # Data cleaning
    df_cleaned = df.dropna()
    df_cleaned.columns = df_cleaned.columns.str.lower()

    # Prepare features
    feature_cols = ['age', 'income']
    X = df_cleaned[feature_cols]
    y = df_cleaned['target']

    return LogisticRegression, StandardScaler, X, y

