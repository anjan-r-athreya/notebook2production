"""Simplified analyzer - just the essential parts for demo."""
import ast
from typing import Dict, List, Set, Any

class CellAnalyzer:
    def __init__(self, cells: List[Dict[str, Any]]):
        self.cells = cells
        self.analysis_results = []

    def analyze_all(self) -> List[Dict[str, Any]]:
        self.analysis_results = []
        for cell in self.cells:
            analysis = self._analyze_cell(cell)
            self.analysis_results.append(analysis)
        self._compute_dependencies()
        return self.analysis_results

    def _analyze_cell(self, cell: Dict[str, Any]) -> Dict[str, Any]:
        source = cell['source']
        analysis = {
            'index': cell['index'],
            'imports': [],
            'variables_defined': set(),
            'variables_used': set(),
            'external_dependencies': set(),  # Variables used before being defined
            'functions_defined': [],
            'hardcoded_values': [],
            'has_hardcoded_paths': False,
            'issues': []
        }

        if not source.strip():
            return analysis

        try:
            tree = ast.parse(source)
            defined_in_cell = set()
            used_before_defined = set()

            # Process statements in order to track what's used vs defined
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        analysis['imports'].extend([a.name for a in node.names])
                        # Imports count as definitions
                        defined_in_cell.update([a.name for a in node.names])
                    else:
                        module = node.module or ''
                        analysis['imports'].append(module)
                        # Track imported names as defined
                        if node.names:
                            for alias in node.names:
                                if alias.name != '*':
                                    defined_in_cell.add(alias.asname if alias.asname else alias.name)
                elif isinstance(node, ast.FunctionDef):
                    analysis['functions_defined'].append(node.name)
                    defined_in_cell.add(node.name)

            # Now do a more careful analysis with statement order
            for stmt in tree.body:
                # Track what's used in this statement
                for node in ast.walk(stmt):
                    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                        var_name = node.id
                        analysis['variables_used'].add(var_name)
                        # If used before being defined, it's an external dependency
                        if var_name not in defined_in_cell:
                            used_before_defined.add(var_name)

                # Track what's defined in this statement
                for node in ast.walk(stmt):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                analysis['variables_defined'].add(target.id)
                                defined_in_cell.add(target.id)
                        # Check for hardcoded paths
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            if '/' in node.value.value or '.csv' in node.value.value or '.pkl' in node.value.value:
                                analysis['has_hardcoded_paths'] = True
                                analysis['hardcoded_values'].append({'type': 'path', 'value': node.value.value})

            # Filter out built-ins and common library functions
            builtins = {'np', 'plt', 'pd', 'print', 'len', 'range', 'enumerate',
                       'zip', 'map', 'filter', 'sum', 'max', 'min', 'abs', 'round',
                       'int', 'float', 'str', 'list', 'dict', 'set', 'tuple',
                       'True', 'False', 'None'}
            analysis['external_dependencies'] = used_before_defined - builtins

        except:
            pass

        return analysis

    def _compute_dependencies(self):
        """Compute dependencies based on external dependencies (variables used before defined)."""
        for i, analysis in enumerate(self.analysis_results):
            analysis['depends_on'] = []

            # Only look at variables that are truly external dependencies
            external_deps = analysis['external_dependencies']

            if not external_deps:
                continue

            # Track which external dependencies we've found
            remaining_deps = external_deps.copy()

            # Look for these dependencies in PRIOR cells (most recent first)
            # This avoids false positives from later cells that redefine the same variables
            for j in range(i - 1, -1, -1):  # Search backwards from current cell
                other = self.analysis_results[j]

                # Check if this prior cell defines any of our remaining external dependencies
                common = remaining_deps & other['variables_defined']
                if common:
                    analysis['depends_on'].append({
                        'cell_index': other['index'],
                        'variables': list(common)
                    })
                    # Remove these from remaining dependencies
                    # (we found the most recent definition)
                    remaining_deps -= common

                # Stop if we've found all dependencies
                if not remaining_deps:
                    break

            # If we still have remaining dependencies, check if they're defined in FUTURE cells
            # This indicates an execution order problem
            if remaining_deps:
                for j in range(i + 1, len(self.analysis_results)):
                    other = self.analysis_results[j]
                    common = remaining_deps & other['variables_defined']
                    if common:
                        analysis['depends_on'].append({
                            'cell_index': other['index'],
                            'variables': list(common)
                        })
                        remaining_deps -= common

    def get_summary(self) -> Dict[str, Any]:
        total_imports = set()
        total_variables = set()
        total_functions = []
        
        for analysis in self.analysis_results:
            total_imports.update(analysis['imports'])
            total_variables.update(analysis['variables_defined'])
            total_functions.extend(analysis['functions_defined'])
        
        issues = []
        
        # Execution order issues
        for analysis in self.analysis_results:
            for dep in analysis['depends_on']:
                if dep['cell_index'] > analysis['index']:
                    issues.append({
                        'type': 'execution_order',
                        'cell': analysis['index'],
                        'message': f"Cell {analysis['index']} depends on cell {dep['cell_index']} which comes later"
                    })
        
        # No functions
        if not total_functions:
            issues.append({
                'type': 'no_functions',
                'message': 'No functions defined - all code is in global scope'
            })
        
        # Hardcoded paths
        cells_with_paths = [a for a in self.analysis_results if a['has_hardcoded_paths']]
        if cells_with_paths:
            issues.append({
                'type': 'hardcoded_paths',
                'cells': [a['index'] for a in cells_with_paths],
                'message': f"{len(cells_with_paths)} cell(s) with hardcoded file paths"
            })
        
        return {
            'total_cells_analyzed': len(self.analysis_results),
            'total_imports': len(total_imports),
            'imports_list': sorted(list(total_imports)),
            'total_variables': len(total_variables),
            'total_functions': len(total_functions),
            'hardcoded_values_count': sum(len(a['hardcoded_values']) for a in self.analysis_results),
            'issues': issues
        }
