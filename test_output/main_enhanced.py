#!/usr/bin/env python3
"""Enhanced main CLI with useful output."""

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
    print()

    # Execute pipeline functions
    LogisticRegression, StandardScaler, X, y = load_data()

    # Show what was loaded
    print(f"✓ Loaded data: {len(X)} samples with {len(X.columns)} features")
    print(f"  Features: {list(X.columns)}")
    print(f"  Target distribution: {y.value_counts().to_dict()}")
    print()

    # Train a simple model to demonstrate
    print("Training model...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_scaled, y)
    score = model.score(X_scaled, y)

    print(f"✓ Model trained successfully")
    print(f"  Training accuracy: {score:.3f}")
    print()

    print("Pipeline completed successfully!")


if __name__ == '__main__':
    main()
