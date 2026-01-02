"""Generate production-ready Python project from extracted functions."""

from typing import Dict, List, Any
from pathlib import Path
import yaml


class ProjectGenerator:
    """Generates a complete Python project from notebook analysis."""

    def __init__(self, functions: List[Dict[str, Any]], imports: List[str],
                 output_dir: str = "./output"):
        """Initialize the generator.

        Args:
            functions: Extracted functions from FunctionExtractor
            imports: List of import statements from analyzer
            output_dir: Directory to generate project in
        """
        self.functions = functions
        self.imports = imports
        self.output_dir = Path(output_dir)

    def generate_project(self) -> None:
        """Generate the complete project structure."""
        # Create directory structure
        self._create_directories()

        # Generate source files
        self._generate_src_modules()

        # Generate config file
        self._generate_config()

        # Generate main CLI
        self._generate_main()

        # Generate requirements
        self._generate_requirements()

        # Generate README
        self._generate_readme()

        print(f"Project generated successfully at: {self.output_dir}")

    def _create_directories(self) -> None:
        """Create the project directory structure."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'src').mkdir(exist_ok=True)

    def _generate_src_modules(self) -> None:
        """Generate Python modules in src/ directory."""
        # Group functions by category
        grouped_functions = self._group_by_category()

        # Generate __init__.py
        self._generate_src_init(grouped_functions)

        # Generate module for each category
        for category, funcs in grouped_functions.items():
            self._generate_module(category, funcs)

    def _group_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group functions by their category.

        Returns:
            Dictionary mapping category to list of functions
        """
        grouped = {}
        for func in self.functions:
            category = func['category']
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(func)

        return grouped

    def _generate_src_init(self, grouped_functions: Dict[str, List[Dict[str, Any]]]) -> None:
        """Generate src/__init__.py with exports."""
        module_names = {
            'data': 'data_processing',
            'feature': 'feature_engineering',
            'model': 'model_training',
            'visualization': 'visualization',
            'utility': 'utils'
        }

        lines = ['"""Main package exports."""', '']

        # Import from each module
        for category, funcs in grouped_functions.items():
            module = module_names.get(category, category)
            func_names = [f['name'] for f in funcs]
            lines.append(f"from .{module} import {', '.join(func_names)}")

        lines.append('')
        lines.append('__all__ = [')
        for funcs in grouped_functions.values():
            for func in funcs:
                lines.append(f"    '{func['name']}',")
        lines.append(']')
        lines.append('')

        init_file = self.output_dir / 'src' / '__init__.py'
        init_file.write_text('\n'.join(lines))

    def _generate_module(self, category: str, functions: List[Dict[str, Any]]) -> None:
        """Generate a Python module for a category of functions.

        Args:
            category: Function category (data, feature, model, etc.)
            functions: List of functions in this category
        """
        module_names = {
            'data': 'data_processing',
            'feature': 'feature_engineering',
            'model': 'model_training',
            'visualization': 'visualization',
            'utility': 'utils'
        }

        module_name = module_names.get(category, category)
        module_path = self.output_dir / 'src' / f'{module_name}.py'

        lines = [
            f'"""Functions for {category} operations."""',
            '',
        ]

        # Add imports needed by these functions
        imports_needed = self._get_imports_for_functions(functions)
        if imports_needed:
            lines.extend(imports_needed)
            lines.append('')

        # Add each function
        for func in functions:
            lines.append(func['full_code'])
            lines.append('')
            lines.append('')

        module_path.write_text('\n'.join(lines))

    def _get_imports_for_functions(self, functions: List[Dict[str, Any]]) -> List[str]:
        """Determine which imports are needed for these functions.

        Args:
            functions: List of functions

        Returns:
            List of import statements
        """
        # For now, include all imports
        # TODO: Parse function code to determine actual imports needed
        import_lines = []

        # Common imports based on what we've seen
        if any('pd.DataFrame' in str(func) for func in functions):
            import_lines.append('import pandas as pd')
        if any('np.ndarray' in str(func) or 'np.' in str(func.get('full_code', '')) for func in functions):
            import_lines.append('import numpy as np')

        # Add typing imports if needed
        has_typing = any(
            'Tuple' in func.get('signature', '') or
            'List' in func.get('signature', '') or
            'Dict' in func.get('signature', '')
            for func in functions
        )
        if has_typing:
            import_lines.insert(0, 'from typing import Tuple, List, Dict, Any')

        return import_lines

    def _generate_config(self) -> None:
        """Generate config.yaml file."""
        config = {
            'description': 'Configuration for generated project',
            'parameters': {
                'note': 'Add configuration parameters here as needed'
            }
        }

        config_path = self.output_dir / 'config.yaml'
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def _generate_main(self) -> None:
        """Generate main.py CLI entry point."""
        lines = [
            '#!/usr/bin/env python3',
            '"""Main CLI entry point for the generated project."""',
            '',
            'import click',
            'import yaml',
            'from pathlib import Path',
            '',
            'from src import *',
            '',
            '',
            '@click.command()',
            '@click.option(\'--config\', default=\'config.yaml\', help=\'Path to config file\')',
            'def main(config):',
            '    """Run the data pipeline."""',
            '    # Load configuration',
            '    config_path = Path(config)',
            '    if config_path.exists():',
            '        with open(config_path) as f:',
            '            cfg = yaml.safe_load(f)',
            '    else:',
            '        cfg = {}',
            '',
            '    print("Running pipeline...")',
            '',
        ]

        # Add function calls in order
        if self.functions:
            lines.append('    # Execute pipeline functions')
            for func in self.functions:
                params = ', '.join(func['parameters']) if func['parameters'] else ''
                if func['returns']:
                    returns = ', '.join(func['returns'])
                    lines.append(f'    {returns} = {func["name"]}({params})')
                else:
                    lines.append(f'    {func["name"]}({params})')
                lines.append('')

        lines.extend([
            '    print("Pipeline completed successfully!")',
            '',
            '',
            'if __name__ == \'__main__\':',
            '    main()',
            ''
        ])

        main_path = self.output_dir / 'main.py'
        main_path.write_text('\n'.join(lines))
        main_path.chmod(0o755)  # Make executable

    def _generate_requirements(self) -> None:
        """Generate requirements.txt from imports."""
        # Map import names to package names
        import_to_package = {
            'pandas': 'pandas',
            'numpy': 'numpy',
            'sklearn': 'scikit-learn',
            'torch': 'torch',
            'tensorflow': 'tensorflow',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
        }

        requirements = set()
        requirements.add('click')  # Always needed for main.py
        requirements.add('pyyaml')  # Always needed for config

        for imp in self.imports:
            # Extract base module name
            base = imp.split('.')[0]
            if base in import_to_package:
                requirements.add(import_to_package[base])

        req_path = self.output_dir / 'requirements.txt'
        req_path.write_text('\n'.join(sorted(requirements)) + '\n')

    def _generate_readme(self) -> None:
        """Generate README.md with usage instructions."""
        lines = [
            '# Generated Project',
            '',
            'This project was automatically generated from a Jupyter notebook using nb2prod.',
            '',
            '## Installation',
            '',
            '```bash',
            'pip install -r requirements.txt',
            '```',
            '',
            '## Usage',
            '',
            '```bash',
            'python main.py --config config.yaml',
            '```',
            '',
            '## Project Structure',
            '',
            '- `src/` - Source code modules',
            '- `config.yaml` - Configuration parameters',
            '- `main.py` - Main CLI entry point',
            '- `requirements.txt` - Python dependencies',
            '',
            '## Generated Functions',
            '',
        ]

        for func in self.functions:
            lines.append(f"### `{func['name']}`")
            lines.append('')
            lines.append(f"Category: {func['category']}")
            if func['parameters']:
                lines.append(f"Parameters: {', '.join(func['parameters'])}")
            if func['returns']:
                lines.append(f"Returns: {', '.join(func['returns'])}")
            lines.append('')

        readme_path = self.output_dir / 'README.md'
        readme_path.write_text('\n'.join(lines))
