"""Functions for model operations."""

from typing import Tuple, List, Dict, Any

def train_model() -> Tuple[Any, Any]:
    """Train and evaluate model.
    
    Returns:
        Tuple containing:
        - test_precision
        - test_recall
    """
    # Calculate metrics
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred)
    test_recall = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)

    print("\n" + "="*50)
    print("MODEL PERFORMANCE METRICS")
    print("="*50)
    print(f"\nTraining Accuracy:   {train_accuracy:.4f}")
    print(f"Test Accuracy:       {test_accuracy:.4f}")
    print(f"\nPrecision:          {test_precision:.4f}")
    print(f"Recall:             {test_recall:.4f}")
    print(f"F1 Score:           {test_f1:.4f}")
    print("\n" + "="*50)

    # Show confusion matrix
    cm = confusion_matrix(y_test, y_test_pred)
    print("\nConfusion Matrix:")
    print(f"                Predicted")
    print(f"              No Churn  Churned")
    print(f"Actual No      {cm[0,0]:6d}   {cm[0,1]:6d}")
    print(f"       Churn   {cm[1,0]:6d}   {cm[1,1]:6d}")

    return test_precision, test_recall

