"""Tests for the project generator."""

import pytest
from pathlib import Path
from generator import ProjectGenerator


def test_generator_initialization(sample_functions, temp_output_dir):
    """Test generator can be initialized."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    assert generator.functions == sample_functions
    assert generator.output_dir == Path(temp_output_dir)


def test_generator_creates_project(sample_functions, temp_output_dir):
    """Test generator creates project structure."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    generator.generate_project()

    output_path = Path(temp_output_dir)

    # Check directory structure
    assert output_path.exists()
    assert (output_path / "src").exists()
    assert (output_path / "main.py").exists()
    assert (output_path / "config.yaml").exists()
    assert (output_path / "requirements.txt").exists()
    assert (output_path / "README.md").exists()


def test_generator_creates_src_modules(sample_functions, temp_output_dir):
    """Test generator creates source modules."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    generator.generate_project()

    src_path = Path(temp_output_dir) / "src"

    assert (src_path / "__init__.py").exists()
    assert (src_path / "data_processing.py").exists()


def test_generator_creates_requirements(sample_functions, temp_output_dir):
    """Test generator creates requirements.txt."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    generator.generate_project()

    req_file = Path(temp_output_dir) / "requirements.txt"
    assert req_file.exists()

    content = req_file.read_text()
    assert "pandas" in content
    assert "numpy" in content
    assert "click" in content


def test_generator_creates_config(sample_functions, temp_output_dir):
    """Test generator creates config.yaml."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    generator.generate_project()

    config_file = Path(temp_output_dir) / "config.yaml"
    assert config_file.exists()


def test_generator_main_is_executable(sample_functions, temp_output_dir):
    """Test generator makes main.py executable."""
    generator = ProjectGenerator(
        functions=sample_functions,
        imports=["pandas", "numpy"],
        output_dir=temp_output_dir,
    )

    generator.generate_project()

    main_file = Path(temp_output_dir) / "main.py"
    assert main_file.exists()

    # Check if file has execute permissions
    import os

    assert os.access(main_file, os.X_OK)
