"""Group notebook cells into logical functions based on dependencies and data flow."""

from typing import Dict, List, Set, Any, Tuple


class CellGrouper:
    """Groups cells into logical units that can become functions."""

    def __init__(self, cells: List[Dict[str, Any]], analysis_results: List[Dict[str, Any]],
                 notebook_stats: Dict[str, int] = None):
        """Initialize the grouper.

        Args:
            cells: Original cell data from parser
            analysis_results: Analysis results from CellAnalyzer
            notebook_stats: Notebook statistics (total_cells, markdown_cells, etc.)
        """
        self.cells = cells
        self.analysis_results = analysis_results
        self.notebook_stats = notebook_stats or {}
        self.groups = []
        self.is_educational = self._detect_educational_notebook()

    def _detect_educational_notebook(self) -> bool:
        """Detect if this notebook is educational/tutorial style.

        Returns:
            True if notebook appears to be educational
        """
        if not self.notebook_stats:
            return False

        # Check markdown ratio (educational notebooks have lots of explanation)
        total_cells = self.notebook_stats.get('total_cells', 1)
        markdown_cells = self.notebook_stats.get('markdown_cells', 0)
        markdown_ratio = markdown_cells / max(total_cells, 1)

        if markdown_ratio > 0.4:  # More than 40% markdown
            return True

        # Check for repetitive variable patterns (indicates parallel examples)
        var_reuse_count = self._count_variable_reuse()
        if var_reuse_count > 3:  # Same variables redefined multiple times
            return True

        # Check for low cross-cell dependencies (self-contained examples)
        cells_with_deps = sum(1 for a in self.analysis_results if a.get('depends_on', []))
        dep_ratio = cells_with_deps / max(len(self.analysis_results), 1)

        if dep_ratio < 0.3:  # Less than 30% of cells depend on others
            return True

        return False

    def _count_variable_reuse(self) -> int:
        """Count how many times the same variables are redefined.

        Returns:
            Maximum reuse count for any variable
        """
        variable_counts = {}

        for analysis in self.analysis_results:
            for var in analysis['variables_defined']:
                variable_counts[var] = variable_counts.get(var, 0) + 1

        if not variable_counts:
            return 0

        # Common tutorial variables
        tutorial_vars = {'x', 'y', 'X', 'data', 'model'}
        max_reuse = 0

        for var in tutorial_vars:
            if var in variable_counts:
                max_reuse = max(max_reuse, variable_counts[var])

        return max_reuse

    def group_cells(self) -> List[Dict[str, Any]]:
        """Group cells into logical function candidates.

        Returns:
            List of cell groups with metadata (empty list if notebook is educational)
        """
        # Don't extract from educational notebooks
        if self.is_educational:
            return []
        # Start with each cell as its own group
        cell_groups = []

        for i, analysis in enumerate(self.analysis_results):
            cell_groups.append({
                'cells': [analysis['index']],
                'analysis': [analysis],
                'variables_defined': analysis['variables_defined'].copy(),
                'external_dependencies': analysis['external_dependencies'].copy(),
                'category': self._categorize_cell(analysis)
            })

        # Merge groups based on dependencies and categories
        merged_groups = self._merge_related_groups(cell_groups)

        # Add metadata to each group and validate quality
        self.groups = []
        for group in merged_groups:
            group_info = self._analyze_group(group)

            # Only include if it's a quality function candidate
            if self._is_quality_function(group_info):
                self.groups.append(group_info)

        return self.groups

    def _categorize_cell(self, analysis: Dict[str, Any]) -> str:
        """Categorize a cell based on its content.

        Args:
            analysis: Cell analysis data

        Returns:
            Category string (import, data, feature, model, visualization, utility)
        """
        # Check for imports
        if analysis['imports'] and not analysis['variables_defined']:
            return 'import'

        # Check for common patterns in variable names
        vars_defined = analysis['variables_defined']
        vars_str = ' '.join(str(v).lower() for v in vars_defined)

        if any(pattern in vars_str for pattern in ['df', 'data', 'dataset', 'load', 'read']):
            return 'data'
        elif any(pattern in vars_str for pattern in ['x_', 'y_', 'feature', 'scaled', 'transform']):
            return 'feature'
        elif any(pattern in vars_str for pattern in ['model', 'train', 'fit', 'predict']):
            return 'model'
        elif any(pattern in vars_str for pattern in ['plot', 'fig', 'ax', 'chart']):
            return 'visualization'
        else:
            return 'utility'

    def _merge_related_groups(self, groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge groups that should be part of the same function.

        Args:
            groups: Initial cell groups

        Returns:
            Merged groups
        """
        if not groups:
            return []

        merged = []
        current_group = groups[0]

        for next_group in groups[1:]:
            # Check if groups should be merged
            should_merge = self._should_merge(current_group, next_group)

            if should_merge:
                # Merge next_group into current_group
                current_group['cells'].extend(next_group['cells'])
                current_group['analysis'].extend(next_group['analysis'])
                current_group['variables_defined'].update(next_group['variables_defined'])
                current_group['external_dependencies'].update(next_group['external_dependencies'])
                # Keep the most specific category
                if next_group['category'] != 'utility' and current_group['category'] == 'utility':
                    current_group['category'] = next_group['category']
            else:
                # Start a new group
                merged.append(current_group)
                current_group = next_group

        # Add the last group
        merged.append(current_group)

        # Filter out import-only groups (they don't need to be functions)
        merged = [g for g in merged if g['category'] != 'import']

        return merged

    def _is_quality_function(self, group_info: Dict[str, Any]) -> bool:
        """Check if a function candidate is high quality and worth extracting.

        Args:
            group_info: Analyzed group information

        Returns:
            True if function is worth extracting
        """
        # Must have at least 2 cells (single cells aren't worth extracting)
        if len(group_info['cells']) < 2:
            return False

        # Must either have parameters OR return values (otherwise it's just isolated code)
        has_io = bool(group_info['parameters']) or bool(group_info['returns'])

        # Or must define at least 2 variables (doing meaningful work)
        does_work = len(group_info['variables_defined']) >= 2

        if not (has_io or does_work):
            return False

        # Check for execution order issues within the group
        for i, cell_idx in enumerate(group_info['cells']):
            # Find the analysis for this cell
            cell_analysis = next((a for a in self.analysis_results if a['index'] == cell_idx), None)
            if not cell_analysis:
                continue

            # Check if this cell depends on later cells IN THE SAME GROUP
            for dep in cell_analysis.get('depends_on', []):
                if dep['cell_index'] in group_info['cells']:
                    # Find position in group
                    dep_position = group_info['cells'].index(dep['cell_index'])
                    if dep_position > i:
                        # Backward dependency within group - bad
                        return False

        return True

    def _has_execution_order_issues(self, group: Dict[str, Any]) -> bool:
        """Check if a group has cells with backward dependencies.

        Args:
            group: Cell group to check

        Returns:
            True if group has execution order issues
        """
        for analysis in group['analysis']:
            # Check if this cell depends on any later cells
            for dep in analysis.get('depends_on', []):
                if dep['cell_index'] > analysis['index']:
                    return True
        return False

    def _should_merge(self, group1: Dict[str, Any], group2: Dict[str, Any]) -> bool:
        """Determine if two groups should be merged.

        Args:
            group1: First group
            group2: Second group

        Returns:
            True if groups should be merged
        """
        max_cell1 = max(group1['cells'])
        min_cell2 = min(group2['cells'])
        gap = min_cell2 - max_cell1

        # Don't merge if groups are too far apart (more than 4 cells between them)
        if gap > 4:
            return False

        # Don't merge if either group has backward dependencies (execution order issues)
        if self._has_execution_order_issues(group1) or self._has_execution_order_issues(group2):
            return False

        # Always merge utility cells if they're adjacent
        if (group1['category'] == 'utility' or group2['category'] == 'utility') and gap <= 2:
            return True

        # Merge if same category and close together
        if group1['category'] == group2['category'] and gap <= 3:
            return True

        # Merge if group2 depends directly on group1's outputs
        group2_deps = group2['external_dependencies']
        group1_outputs = group1['variables_defined']

        if group2_deps & group1_outputs:
            # They share variables - merge if sequential and categories are compatible
            if gap <= 2:
                compatible_categories = {
                    ('data', 'data'),
                    ('data', 'feature'),
                    ('feature', 'feature'),
                    ('feature', 'model'),
                    ('data', 'model'),
                    ('model', 'model'),
                    ('utility', 'data'),
                    ('utility', 'feature'),
                    ('utility', 'model'),
                    ('data', 'utility'),
                    ('feature', 'utility'),
                    ('model', 'utility')
                }
                category_pair = (group1['category'], group2['category'])
                if category_pair in compatible_categories:
                    return True

        return False

    def _analyze_group(self, group: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a group to extract function metadata.

        Args:
            group: Cell group

        Returns:
            Group with added metadata
        """
        cells = group['cells']
        analyses = group['analysis']

        # Collect all variables defined and used in the group
        all_defined = set()
        all_external = set()

        for analysis in analyses:
            all_defined.update(analysis['variables_defined'])
            all_external.update(analysis['external_dependencies'])

        # Collect all imports from the entire notebook to exclude from parameters
        all_imports = set()
        for result in self.analysis_results:
            all_imports.update(result['imports'])
            # Also add common imported names
            for imp in result['imports']:
                # Extract module/function names from imports
                if '.' in imp:
                    parts = imp.split('.')
                    all_imports.update(parts)

        # Parameters are external dependencies that are NOT:
        # 1. Defined within the group
        # 2. Imported from modules
        parameters = all_external - all_defined - all_imports

        # Returns are variables defined that are used by later cells
        # (we'll need to check this against cells that come after the group)
        max_cell_index = max(cells)
        returns = set()

        for later_analysis in self.analysis_results:
            if later_analysis['index'] > max_cell_index:
                # Check if this later cell uses any of our defined variables
                used_vars = later_analysis['external_dependencies']
                returns.update(all_defined & used_vars)

        return {
            'cells': cells,
            'category': group['category'],
            'parameters': sorted(list(parameters)),
            'returns': sorted(list(returns)),
            'variables_defined': sorted(list(all_defined)),
            'suggested_name': self._suggest_function_name(group['category'], parameters, returns)
        }

    def _suggest_function_name(self, category: str, parameters: Set[str],
                               returns: Set[str]) -> str:
        """Suggest a function name based on the group's purpose.

        Args:
            category: Cell category
            parameters: Input parameters
            returns: Return values

        Returns:
            Suggested function name
        """
        # Base name from category
        base_names = {
            'data': 'load_data',
            'feature': 'engineer_features',
            'model': 'train_model',
            'visualization': 'create_visualization',
            'utility': 'process_data'
        }

        base_name = base_names.get(category, 'process')

        # Make more specific based on returns
        return_str = ' '.join(str(r).lower() for r in returns) if returns else ''

        if category == 'data':
            if 'clean' in return_str or 'processed' in return_str:
                return 'load_and_clean_data'
            return 'load_data'
        elif category == 'feature':
            if 'scaled' in return_str or 'normalized' in return_str:
                return 'scale_features'
            return 'engineer_features'
        elif category == 'model':
            if 'predict' in return_str:
                return 'make_predictions'
            elif 'evaluate' in return_str:
                return 'evaluate_model'
            return 'train_model'

        return base_name
