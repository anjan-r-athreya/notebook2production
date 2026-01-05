"""Functions for data operations."""

from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np

def load_data() -> Tuple[np.ndarray, pd.DataFrame, List[Any], np.ndarray]:
    """Load and preprocess data.
    
    Returns:
        Tuple containing:
        - X
        - df
        - feature_columns
        - y
    """
    # Generate synthetic customer data
    np.random.seed(42)
    n_customers = 1000

    data = {
        'customer_id': range(1, n_customers + 1),
        'account_length': np.random.randint(1, 200, n_customers),
        'total_charges': np.random.uniform(50, 5000, n_customers),
        'monthly_charges': np.random.uniform(20, 150, n_customers),
        'num_products': np.random.randint(1, 5, n_customers),
        'support_calls': np.random.randint(0, 10, n_customers),
        'contract_type': np.random.choice(['monthly', 'annual', 'biannual'], n_customers),
    }

    df = pd.DataFrame(data)

    # Create churn target based on features (customers with high support calls and short contracts more likely to churn)
    churn_probability = (
        0.3 * (df['support_calls'] > 5).astype(int) +
        0.2 * (df['contract_type'] == 'monthly').astype(int) +
        0.2 * (df['account_length'] < 50).astype(int) +
        0.15 * (df['monthly_charges'] > 100).astype(int) +
        0.15 * (df['num_products'] == 1).astype(int)
    )

    df['churned'] = (churn_probability + np.random.uniform(-0.2, 0.2, n_customers) > 0.5).astype(int)

    # Data cleaning and preprocessing
    df_clean = df.copy()
    df_clean['avg_monthly_charge'] = df_clean['total_charges'] / df_clean['account_length']
    df_clean['calls_per_month'] = df_clean['support_calls'] / (df_clean['account_length'] / 30)
    df_clean = pd.get_dummies(df_clean, columns=['contract_type'], drop_first=True)

    print(f"Dataset shape: {df_clean.shape}")
    print(f"Churn rate: {df_clean['churned'].mean():.2%}")

    # Prepare features and target
    feature_columns = [
        'account_length', 'total_charges', 'monthly_charges',
        'num_products', 'support_calls', 'avg_monthly_charge',
        'calls_per_month', 'contract_type_biannual', 'contract_type_monthly'
    ]

    X = df_clean[feature_columns]
    y = df_clean['churned']

    return X, df, feature_columns, y

