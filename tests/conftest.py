"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import json
import tempfile
import shutil


@pytest.fixture
def sample_notebook():
    """Create a sample notebook for testing."""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Test Notebook\n", "This is a test notebook."],
            },
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "source": ["import pandas as pd\n", "import numpy as np"],
                "outputs": [],
            },
            {
                "cell_type": "code",
                "execution_count": 2,
                "metadata": {},
                "source": [
                    "def load_data():\n",
                    "    return pd.DataFrame({'a': [1, 2, 3]})",
                ],
                "outputs": [],
            },
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "source": ["df = load_data()\n", "print(df.head())"],
                "outputs": [],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.8.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    # Create temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False) as f:
        json.dump(notebook, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_functions():
    """Sample extracted functions for testing."""
    return [
        {
            "name": "load_data",
            "category": "data",
            "parameters": [],
            "returns": ["df"],
            "cells": [2],
            "signature": "def load_data() -> Any:",
            "full_code": 'def load_data():\n    """Load sample data."""\n    return pd.DataFrame({"a": [1, 2, 3]})',
            "docstring": "Load sample data.",
        },
        {
            "name": "process_data",
            "category": "data",
            "parameters": ["df"],
            "returns": ["processed_df"],
            "cells": [3],
            "signature": "def process_data(df) -> Any:",
            "full_code": 'def process_data(df):\n    """Process data."""\n    return df.copy()',
            "docstring": "Process data.",
        },
    ]
