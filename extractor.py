"""Extract function signatures and code from grouped cells."""

from typing import Dict, List, Any, Tuple
import ast


class FunctionExtractor:
    """Extracts functions from grouped notebook cells."""

    def __init__(self, cells: List[Dict[str, Any]], groups: List[Dict[str, Any]]):
        """Initialize the extractor.

        Args:
            cells: Original cell data from parser
            groups: Cell groups from CellGrouper
        """
        self.cells = cells
        self.groups = groups
        self.functions = []

    def extract_functions(self) -> List[Dict[str, Any]]:
        """Extract function definitions from cell groups.

        Returns:
            List of function definitions with signatures and code
        """
        self.functions = []

        for group in self.groups:
            func_def = self._create_function(group)
            self.functions.append(func_def)

        return self.functions

    def _create_function(self, group: Dict[str, Any]) -> Dict[str, Any]:
        """Create a function definition from a cell group.

        Args:
            group: Cell group metadata

        Returns:
            Function definition with signature and body
        """
        func_name = group['suggested_name']
        parameters = group['parameters']
        returns = group['returns']
        cells = group['cells']

        # Get the source code from all cells in the group
        cell_sources = []
        for cell_index in cells:
            # Find the cell with this index
            cell = self._get_cell_by_index(cell_index)
            if cell and cell['source'].strip():
                cell_sources.append(cell['source'])

        # Combine cell source code
        combined_source = '\n\n'.join(cell_sources)

        # Generate function signature
        signature = self._generate_signature(func_name, parameters, returns)

        # Generate function body with proper indentation
        body = self._generate_body(combined_source, parameters, returns)

        # Generate docstring
        docstring = self._generate_docstring(func_name, group['category'], parameters, returns)

        return {
            'name': func_name,
            'category': group['category'],
            'signature': signature,
            'docstring': docstring,
            'body': body,
            'parameters': parameters,
            'returns': returns,
            'cells': cells,
            'full_code': self._assemble_function(signature, docstring, body)
        }

    def _get_cell_by_index(self, index: int) -> Dict[str, Any]:
        """Get cell data by its index.

        Args:
            index: Cell index

        Returns:
            Cell data or None
        """
        for cell in self.cells:
            if cell['index'] == index:
                return cell
        return None

    def _generate_signature(self, func_name: str, parameters: List[str],
                           returns: List[str]) -> str:
        """Generate function signature.

        Args:
            func_name: Function name
            parameters: List of parameter names
            returns: List of return value names

        Returns:
            Function signature string
        """
        # Build parameter list
        if parameters:
            params_str = ', '.join(parameters)
        else:
            params_str = ''

        # Add return type hint if we have returns
        if returns:
            if len(returns) == 1:
                return_hint = f" -> {self._infer_type(returns[0])}"
            else:
                types = [self._infer_type(r) for r in returns]
                return_hint = f" -> Tuple[{', '.join(types)}]"
        else:
            return_hint = ""

        return f"def {func_name}({params_str}){return_hint}:"

    def _infer_type(self, var_name: str) -> str:
        """Infer type hint from variable name.

        Args:
            var_name: Variable name

        Returns:
            Type hint string
        """
        var_lower = var_name.lower()

        # DataFrame patterns
        if 'df' in var_lower or 'dataframe' in var_lower:
            return 'pd.DataFrame'
        elif 'data' in var_lower and not ('path' in var_lower or 'file' in var_lower):
            return 'pd.DataFrame'

        # Array patterns
        elif var_lower.startswith('x_') or var_lower.startswith('y_') or var_lower == 'x' or var_lower == 'y':
            return 'np.ndarray'
        elif 'array' in var_lower or 'matrix' in var_lower:
            return 'np.ndarray'

        # String patterns
        elif 'path' in var_lower or 'file' in var_lower or 'filename' in var_lower:
            return 'str'
        elif 'name' in var_lower or 'title' in var_lower or 'label' in var_lower:
            return 'str'

        # Numeric patterns
        elif any(word in var_lower for word in ['epoch', 'iteration', 'batch', 'size', 'count', 'num']):
            return 'int'
        elif any(word in var_lower for word in ['rate', 'alpha', 'beta', 'loss', 'score', 'accuracy']):
            return 'float'

        # Model/transformer patterns
        elif 'model' in var_lower or 'estimator' in var_lower:
            return 'Any'
        elif 'scaler' in var_lower or 'encoder' in var_lower or 'transform' in var_lower:
            return 'Any'

        # Collection patterns
        elif 'list' in var_lower or var_lower.endswith('s') and len(var_lower) > 2:
            return 'List[Any]'
        elif 'dict' in var_lower or 'config' in var_lower:
            return 'Dict[str, Any]'

        else:
            return 'Any'

    def _generate_docstring(self, func_name: str, category: str,
                           parameters: List[str], returns: List[str]) -> str:
        """Generate function docstring.

        Args:
            func_name: Function name
            category: Function category
            parameters: Parameter names
            returns: Return value names

        Returns:
            Docstring text
        """
        # Create a brief description based on category
        descriptions = {
            'data': 'Load and preprocess data.',
            'feature': 'Engineer features from data.',
            'model': 'Train and evaluate model.',
            'visualization': 'Create visualization.',
            'utility': 'Process data.'
        }

        description = descriptions.get(category, 'Process data.')

        lines = [f'"""{description}']

        # Add parameters section
        if parameters:
            lines.append('')
            lines.append('Args:')
            for param in parameters:
                param_type = self._infer_type(param)
                lines.append(f'    {param}: {param_type}')

        # Add returns section
        if returns:
            lines.append('')
            if len(returns) == 1:
                lines.append('Returns:')
                return_type = self._infer_type(returns[0])
                lines.append(f'    {return_type}')
            else:
                lines.append('Returns:')
                lines.append('    Tuple containing:')
                for ret in returns:
                    lines.append(f'    - {ret}')

        lines.append('"""')
        return '\n    '.join(lines)

    def _generate_body(self, source: str, parameters: List[str],
                      returns: List[str]) -> str:
        """Generate function body from source code.

        Args:
            source: Combined source code from cells
            parameters: Function parameters
            returns: Return values

        Returns:
            Indented function body
        """
        # Indent all lines
        lines = source.split('\n')
        indented = ['    ' + line if line.strip() else '' for line in lines]

        # Add return statement if needed
        if returns:
            indented.append('')
            if len(returns) == 1:
                indented.append(f'    return {returns[0]}')
            else:
                returns_str = ', '.join(returns)
                indented.append(f'    return {returns_str}')

        return '\n'.join(indented)

    def _assemble_function(self, signature: str, docstring: str, body: str) -> str:
        """Assemble complete function code.

        Args:
            signature: Function signature
            docstring: Function docstring
            body: Function body

        Returns:
            Complete function code
        """
        return f"{signature}\n    {docstring}\n{body}"
