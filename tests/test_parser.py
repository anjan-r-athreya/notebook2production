"""Tests for the notebook parser."""

import pytest
from nb2prod.parser import NotebookParser


def test_parser_initialization(sample_notebook):
    """Test parser can be initialized with a notebook."""
    parser = NotebookParser(sample_notebook)
    assert str(parser.notebook_path) == sample_notebook


def test_parser_parses_notebook(sample_notebook):
    """Test parser can parse a notebook."""
    parser = NotebookParser(sample_notebook)
    data = parser.parse()

    assert "stats" in data
    assert "code_cells" in data["stats"]
    assert "markdown_cells" in data["stats"]
    assert "total_cells" in data["stats"]


def test_parser_gets_code_cells(sample_notebook):
    """Test parser extracts code cells."""
    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    assert len(code_cells) == 3
    assert "source" in code_cells[0]


def test_parser_invalid_file():
    """Test parser handles invalid file path."""
    with pytest.raises(Exception):
        parser = NotebookParser("nonexistent.ipynb")
        parser.parse()


def test_parser_stats(sample_notebook):
    """Test parser calculates correct stats."""
    parser = NotebookParser(sample_notebook)
    data = parser.parse()
    stats = data["stats"]

    assert stats["code_cells"] == 3
    assert stats["markdown_cells"] == 1
    assert stats["total_cells"] == 4
