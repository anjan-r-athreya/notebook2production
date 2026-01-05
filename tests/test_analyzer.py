"""Tests for the cell analyzer."""

import pytest
from simple_analyze import CellAnalyzer


def test_analyzer_initialization(sample_notebook):
    """Test analyzer can be initialized."""
    from parser import NotebookParser

    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    analyzer = CellAnalyzer(code_cells)
    assert analyzer.cells == code_cells


def test_analyzer_analyzes_cells(sample_notebook):
    """Test analyzer can analyze all cells."""
    from parser import NotebookParser

    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    analyzer = CellAnalyzer(code_cells)
    results = analyzer.analyze_all()

    assert len(results) == len(code_cells)
    assert all("index" in r for r in results)


def test_analyzer_gets_summary(sample_notebook):
    """Test analyzer produces summary."""
    from parser import NotebookParser

    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    analyzer = CellAnalyzer(code_cells)
    analyzer.analyze_all()
    summary = analyzer.get_summary()

    assert "total_imports" in summary
    assert "total_functions" in summary
    assert "imports_list" in summary
    assert "issues" in summary


def test_analyzer_detects_imports(sample_notebook):
    """Test analyzer detects imports."""
    from parser import NotebookParser

    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    analyzer = CellAnalyzer(code_cells)
    analyzer.analyze_all()
    summary = analyzer.get_summary()

    assert "pandas" in summary["imports_list"]
    assert "numpy" in summary["imports_list"]


def test_analyzer_detects_functions(sample_notebook):
    """Test analyzer detects function definitions."""
    from parser import NotebookParser

    parser = NotebookParser(sample_notebook)
    parser.parse()
    code_cells = parser.get_code_cells()

    analyzer = CellAnalyzer(code_cells)
    results = analyzer.analyze_all()
    summary = analyzer.get_summary()

    # Should detect at least one function
    assert summary["total_functions"] >= 1
