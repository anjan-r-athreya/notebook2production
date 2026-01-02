#!/usr/bin/env python3
"""Demo of nb2prod Phase 1 functionality."""

from pathlib import Path
import sys

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from parser import NotebookParser
from simple_analyze import CellAnalyzer

print("=" * 60)
print("nb2prod Phase 1 Demo")
print("=" * 60)

# Parse notebook
notebook_path = current_dir / 'test_notebook.ipynb'
print(f"\n🔍 Analyzing notebook: {notebook_path.name}\n")
parser = NotebookParser(str(notebook_path))
data = parser.parse()

# Display structure
stats = data['stats']
print("📊 Notebook Structure:")
print(f"   ├─ {stats['code_cells']} code cells")
print(f"   ├─ {stats['markdown_cells']} markdown cells")
print(f"   └─ {stats['empty_cells']} empty cells")

# Analyze
code_cells = parser.get_code_cells()
analyzer = CellAnalyzer(code_cells)
results = analyzer.analyze_all()
summary = analyzer.get_summary()

# Display summary
print(f"\n📦 Code Analysis:")
print(f"   ├─ {summary['total_imports']} imports detected")
print(f"   ├─ {summary['total_variables']} variables defined")
print(f"   ├─ {summary['total_functions']} functions defined")
print(f"   └─ {summary['hardcoded_values_count']} hardcoded values detected")

if summary['imports_list']:
    print(f"\nImports: {', '.join(summary['imports_list'][:10])}")

# Display issues
issues = summary['issues']
if issues:
    print(f"\n⚠️  Issues Found ({len(issues)}):")
    for issue in issues:
        issue_type = issue['type']
        if issue_type == 'execution_order':
            print(f"\n  • Execution Order Issue:")
            print(f"    {issue['message']}")
        elif issue_type == 'hardcoded_paths':
            print(f"\n  • {issue['message']}")
            cells_str = ', '.join(map(str, issue['cells'][:5]))
            print(f"    Cells: {cells_str}")
        elif issue_type == 'no_functions':
            print(f"\n  • {issue['message']}")

# Calculate score
score = 10
for issue in issues:
    if issue['type'] == 'execution_order':
        score -= 2
    elif issue['type'] == 'hardcoded_paths':
        score -= 2
    elif issue['type'] == 'no_functions':
        score -= 3
score = max(0, min(10, score))

if score >= 8:
    emoji = "🎉"
elif score >= 5:
    emoji = "⚠️"
else:
    emoji = "❌"

print(f"\n{emoji} Production Readiness Score: {score}/10")

print("\n" + "=" * 60)
print("✓ Phase 1 Complete! Parser and Analyzer working correctly.")
print("=" * 60)
