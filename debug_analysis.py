from parser import NotebookParser
from simple_analyze import CellAnalyzer

parser = NotebookParser('clean_notebook.ipynb')
data = parser.parse()
code_cells = parser.get_code_cells()

analyzer = CellAnalyzer(code_cells)
results = analyzer.analyze_all()

# Print cells 7, 8, 9
for cell_idx in [7, 8, 9]:
    for r in results:
        if r['index'] == cell_idx:
            print(f"\nCell {cell_idx}:")
            print(f"  variables_defined: {r['variables_defined']}")
            print(f"  external_dependencies: {r['external_dependencies']}")
            break
