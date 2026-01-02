"""Notebook parsing with nbformat."""

import nbformat
from pathlib import Path
from typing import Dict, List, Any


class NotebookParser:
    """Parse Jupyter notebooks and extract cell information."""

    def __init__(self, notebook_path: str):
        """Initialize parser with notebook path.

        Args:
            notebook_path: Path to .ipynb file
        """
        self.notebook_path = Path(notebook_path)
        self.notebook = None
        self.cells = []

    def parse(self) -> Dict[str, Any]:
        """Parse the notebook and extract information.

        Returns:
            Dictionary with notebook metadata and cells

        Raises:
            FileNotFoundError: If notebook file doesn't exist
            ValueError: If file is not a valid notebook
        """
        if not self.notebook_path.exists():
            raise FileNotFoundError(f"Notebook not found: {self.notebook_path}")

        # Read notebook
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = nbformat.read(f, as_version=4)

        # Extract cells
        self.cells = self._extract_cells()

        return {
            'path': str(self.notebook_path),
            'cells': self.cells,
            'metadata': self.notebook.get('metadata', {}),
            'stats': self._get_stats()
        }

    def _extract_cells(self) -> List[Dict[str, Any]]:
        """Extract cell information from notebook.

        Returns:
            List of cell dictionaries with type, source, and metadata
        """
        cells = []
        for idx, cell in enumerate(self.notebook.cells):
            cell_data = {
                'index': idx,
                'type': cell.cell_type,
                'source': cell.source,
                'execution_count': cell.get('execution_count'),
                'outputs': []
            }

            # Extract outputs for code cells
            if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
                cell_data['outputs'] = [
                    {
                        'output_type': output.get('output_type'),
                        'data': output.get('data', {}),
                        'text': output.get('text', '')
                    }
                    for output in cell.outputs
                ]

            cells.append(cell_data)

        return cells

    def _get_stats(self) -> Dict[str, int]:
        """Get statistics about the notebook.

        Returns:
            Dictionary with counts of different cell types and elements
        """
        code_cells = [c for c in self.cells if c['type'] == 'code']
        markdown_cells = [c for c in self.cells if c['type'] == 'markdown']

        return {
            'total_cells': len(self.cells),
            'code_cells': len(code_cells),
            'markdown_cells': len(markdown_cells),
            'empty_cells': sum(1 for c in self.cells if not c['source'].strip())
        }

    def get_code_cells(self) -> List[Dict[str, Any]]:
        """Get only code cells from the notebook.

        Returns:
            List of code cell dictionaries
        """
        return [c for c in self.cells if c['type'] == 'code' and c['source'].strip()]
