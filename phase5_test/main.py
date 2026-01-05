#!/usr/bin/env python3
"""Main CLI entry point for the generated project."""

import click
import yaml
from pathlib import Path

from src import *


@click.command()
@click.option('--config', default='config.yaml', help='Path to config file')
def main(config):
    """Run the data pipeline."""
    # Load configuration
    config_path = Path(config)
    if config_path.exists():
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {}

    print("Running pipeline...")

    # Execute pipeline functions
    X, df, feature_columns, y = load_data()

    X_test, model, y_test, y_test_pred, y_test_proba, y_train, y_train_pred = engineer_features()

    test_precision, test_recall = train_model()

    engineer_features(customer, idx)

    print("Pipeline completed successfully!")


if __name__ == '__main__':
    main()
