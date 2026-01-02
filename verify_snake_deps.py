from parser import NotebookParser
from simple_analyze import CellAnalyzer

parser = NotebookParser('Notebooks/Snake.ipynb')
data = parser.parse()
code_cells = parser.get_code_cells()

analyzer = CellAnalyzer(code_cells)
results = analyzer.analyze_all()

# Check the three flagged cells
print("CELL 5 (QTrainer class):")
for r in results:
    if r['index'] == 5:
        print(f"  Defines: {r['variables_defined']}")
        print(f"  External deps: {r['external_dependencies']}")
        print(f"  Depends on cells: {r['depends_on']}")
        break

print("\nCELL 8 (SnakeGameAI class):")
for r in results:
    if r['index'] == 8:
        print(f"  Defines: {sorted(list(r['variables_defined']))[:10]}...")  # Just show first 10
        break

print("\nCELL 11 (Agent class):")
for r in results:
    if r['index'] == 11:
        print(f"  Defines: {r['variables_defined']}")
        print(f"  External deps: {r['external_dependencies']}")
        print(f"  Depends on cells: {r['depends_on']}")
        break

print("\nCELL 13 (plot function):")
for r in results:
    if r['index'] == 13:
        print(f"  Defines: {r['variables_defined']}")
        print(f"  External deps: {r['external_dependencies']}")
        print(f"  Depends on cells: {r['depends_on']}")
        break

print("\nCELL 15 (train_agent function):")
for r in results:
    if r['index'] == 15:
        print(f"  Defines: {sorted(list(r['variables_defined']))[:10]}...")
        break

print("\nCELL 17 (calling train_agent):")
for r in results:
    if r['index'] == 17:
        print(f"  Defines: {r['variables_defined']}")
        print(f"  External deps: {r['external_dependencies']}")
        print(f"  Depends on cells: {r['depends_on']}")
        break
