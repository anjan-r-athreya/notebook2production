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
    LogisticRegression, StandardScaler, X, y = load_data()

    print("Pipeline completed successfully!")


if __name__ == '__main__':
    main()
