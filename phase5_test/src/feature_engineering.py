"""Functions for feature operations."""

from typing import Tuple, List, Dict, Any
import pandas as pd
import numpy as np

def engineer_features() -> Tuple[np.ndarray, Any, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Engineer features from data.
    
    Returns:
        Tuple containing:
        - X_test
        - model
        - y_test
        - y_test_pred
        - y_test_proba
        - y_train
        - y_train_pred
    """
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    print("Training model...")
    model.fit(X_train_scaled, y_train)
    print("Model training complete!")

    # Make predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    y_test_proba = model.predict_proba(X_test_scaled)[:, 1]

    return X_test, model, y_test, y_test_pred, y_test_proba, y_train, y_train_pred


def engineer_features(customer, idx):
    """Engineer features from data.
    
    Args:
        customer: Any
        idx: Any
    """
    # Feature importance analysis
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nTop 5 Most Important Features:")
    print("="*50)
    for idx, row in feature_importance.head(5).iterrows():
        print(f"{row['feature']:25s} {row['importance']:.4f}")

    # Predict on new customers
    print("\n" + "="*50)
    print("PREDICTIONS ON HIGH-RISK CUSTOMERS")
    print("="*50)

    # Find customers with high churn probability
    high_risk_idx = np.where(y_test_proba > 0.7)[0]
    high_risk_customers = X_test.iloc[high_risk_idx]

    print(f"\nFound {len(high_risk_customers)} high-risk customers (>70% churn probability)")
    print("\nSample high-risk customer profiles:")
    for i, (idx, customer) in enumerate(high_risk_customers.head(3).iterrows()):
        prob = y_test_proba[high_risk_idx[i]]
        print(f"\nCustomer {idx}:")
        print(f"  Churn Probability: {prob:.2%}")
        print(f"  Account Length: {customer['account_length']:.0f} days")
        print(f"  Support Calls: {customer['support_calls']:.0f}")
        print(f"  Monthly Charges: ${customer['monthly_charges']:.2f}")

    # Summary statistics
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"\nTotal customers analyzed: {len(df)}")
    print(f"Actual churn rate: {y_test.mean():.2%}")
    print(f"Predicted churn rate: {y_test_pred.mean():.2%}")
    print(f"\nModel correctly identified {test_recall:.2%} of actual churners")
    print(f"Of predicted churners, {test_precision:.2%} actually churned")
    print(f"\nHigh-risk customers to follow up with: {len(high_risk_customers)}")

