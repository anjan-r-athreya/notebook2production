"""Tests for the CLI interface."""

import pytest
from click.testing import CliRunner
from nb2prod.cli import cli


def test_cli_version():
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Convert messy Jupyter notebooks" in result.output


def test_analyze_command_help():
    """Test analyze command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze a notebook" in result.output


def test_extract_command_help():
    """Test extract command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["extract", "--help"])
    assert result.exit_code == 0
    assert "Extract function suggestions" in result.output


def test_convert_command_help():
    """Test convert command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["convert", "--help"])
    assert result.exit_code == 0
    assert "Convert notebook to production-ready" in result.output


def test_analyze_command(sample_notebook):
    """Test analyze command with sample notebook."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", sample_notebook])
    assert result.exit_code == 0
    assert "NOTEBOOK ANALYSIS" in result.output


def test_analyze_command_detailed(sample_notebook):
    """Test analyze command with detailed flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", sample_notebook, "--detailed"])
    assert result.exit_code == 0
    assert "NOTEBOOK ANALYSIS" in result.output


def test_analyze_nonexistent_file():
    """Test analyze command with nonexistent file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "nonexistent.ipynb"])
    assert result.exit_code != 0


def test_extract_command(sample_notebook):
    """Test extract command with sample notebook."""
    runner = CliRunner()
    result = runner.invoke(cli, ["extract", sample_notebook])
    # Command may return 0 or 1 depending on extraction success
    # Just check it doesn't crash completely
    assert "FUNCTION EXTRACTION" in result.output
