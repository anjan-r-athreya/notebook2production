"""LLM-powered code enhancement using Claude API."""

import os
from typing import Dict, List, Any, Optional
import anthropic


class LLMRefactor:
    """Uses Claude to improve extracted functions and fix dependencies."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the LLM refactor.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def enhance_functions(
        self,
        functions: List[Dict[str, Any]],
        notebook_context: str = ""
    ) -> List[Dict[str, Any]]:
        """Enhance extracted functions using Claude.

        Args:
            functions: List of extracted functions from FunctionExtractor
            notebook_context: Optional context about the notebook

        Returns:
            Enhanced functions with improved names, parameters, and code
        """
        enhanced_functions = []

        for i, func in enumerate(functions):
            print(f"Enhancing function {i+1}/{len(functions)}: {func['name']}")

            try:
                enhanced = self._enhance_single_function(func, functions, notebook_context)
                enhanced_functions.append(enhanced)
            except Exception as e:
                print(f"  Warning: Enhancement failed, using original: {e}")
                enhanced_functions.append(func)

        # Fix cross-function dependencies
        enhanced_functions = self._fix_dependencies(enhanced_functions)

        return enhanced_functions

    def _enhance_single_function(
        self,
        func: Dict[str, Any],
        all_functions: List[Dict[str, Any]],
        notebook_context: str
    ) -> Dict[str, Any]:
        """Enhance a single function using Claude.

        Args:
            func: Function to enhance
            all_functions: All functions for context
            notebook_context: Notebook context

        Returns:
            Enhanced function
        """
        # Build context about other functions
        other_funcs_context = self._build_function_context(all_functions, func)

        prompt = f"""You are enhancing a function extracted from a Jupyter notebook.

CURRENT FUNCTION:
{func['full_code']}

FUNCTION METADATA:
- Category: {func['category']}
- Parameters: {func['parameters']}
- Returns: {func['returns']}
- Source cells: {func['cells']}

OTHER FUNCTIONS IN PIPELINE:
{other_funcs_context}

TASK:
1. Improve the function name to be more descriptive
2. Fix parameters - add missing parameters that are used but not defined
3. Fix return values to match what's actually returned
4. Add a clear, helpful docstring
5. Ensure the function is self-contained and runnable

IMPORTANT:
- If the function uses variables from OTHER functions, add them as parameters
- Keep all the original code logic intact
- Only improve structure, naming, and documentation
- Return valid Python code

Respond with a JSON object:
{{
  "name": "improved_function_name",
  "parameters": ["param1", "param2"],
  "returns": ["return1", "return2"],
  "docstring": "Clear description of what this function does",
  "code": "complete Python function code"
}}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse Claude's response
        result = self._parse_llm_response(response.content[0].text)

        # Update function with enhanced version
        enhanced = func.copy()
        enhanced['name'] = result.get('name', func['name'])
        enhanced['parameters'] = result.get('parameters', func['parameters'])
        enhanced['returns'] = result.get('returns', func['returns'])
        enhanced['docstring'] = result.get('docstring', func.get('docstring', ''))
        enhanced['full_code'] = result.get('code', func['full_code'])

        # Regenerate signature
        enhanced['signature'] = self._generate_signature(
            enhanced['name'],
            enhanced['parameters'],
            enhanced['returns']
        )

        return enhanced

    def _build_function_context(
        self,
        all_functions: List[Dict[str, Any]],
        current_func: Dict[str, Any]
    ) -> str:
        """Build context string about other functions.

        Args:
            all_functions: All functions
            current_func: Current function being enhanced

        Returns:
            Context string
        """
        context_parts = []

        for func in all_functions:
            if func == current_func:
                continue

            context_parts.append(
                f"Function: {func['name']}\n"
                f"  Returns: {', '.join(func['returns']) if func['returns'] else 'None'}\n"
                f"  Category: {func['category']}"
            )

        return "\n\n".join(context_parts) if context_parts else "No other functions"

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Claude.

        Args:
            response_text: Response text from Claude

        Returns:
            Parsed dictionary
        """
        import json
        import re

        # Try to extract JSON from response
        # Claude might wrap it in markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                raise ValueError("Could not find JSON in LLM response")

        return json.loads(json_str)

    def _generate_signature(
        self,
        name: str,
        parameters: List[str],
        returns: List[str]
    ) -> str:
        """Generate function signature.

        Args:
            name: Function name
            parameters: Parameter names
            returns: Return value names

        Returns:
            Signature string
        """
        params_str = ', '.join(parameters) if parameters else ''

        if returns:
            if len(returns) == 1:
                return_hint = " -> Any"
            else:
                return_hint = " -> Tuple"
        else:
            return_hint = ""

        return f"def {name}({params_str}){return_hint}:"

    def _fix_dependencies(
        self,
        functions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fix cross-function dependencies.

        Ensures functions receive outputs from previous functions as parameters.

        Args:
            functions: List of enhanced functions

        Returns:
            Functions with fixed dependencies
        """
        # Build a map of what each function returns
        available_vars = {}  # var_name -> function_index

        for i, func in enumerate(functions):
            for ret in func['returns']:
                available_vars[ret] = i

        # Update parameters for each function based on what it needs
        for i, func in enumerate(functions):
            needed_vars = set(func['parameters'])

            # Check which needed vars are available from previous functions
            for var in needed_vars:
                if var in available_vars and available_vars[var] < i:
                    # This var is available from an earlier function
                    if var not in func['parameters']:
                        func['parameters'].append(var)

        return functions

    def generate_enhanced_main(
        self,
        functions: List[Dict[str, Any]],
        imports: List[str]
    ) -> str:
        """Generate an enhanced main.py with proper function chaining.

        Args:
            functions: Enhanced functions
            imports: Import statements

        Returns:
            main.py content
        """
        prompt = f"""Generate a main.py file that orchestrates these functions in a data pipeline.

FUNCTIONS:
{self._format_functions_for_prompt(functions)}

REQUIREMENTS:
1. Import all functions from src
2. Chain functions properly - pass outputs from one function as inputs to the next
3. Print useful progress messages and results
4. Use Click for CLI
5. Load config from YAML

Generate a complete, working main.py file."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract code from response
        code = response.content[0].text

        # Try to extract Python code if wrapped in markdown
        import re

        # Try ```python first
        code_match = re.search(r'```python\s*\n(.*?)\n```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1)
        else:
            # Try generic ``` code blocks
            code_match = re.search(r'```\s*\n(.*?)\n```', code, re.DOTALL)
            if code_match:
                code = code_match.group(1)
            else:
                # If no code blocks found, strip leading/trailing markdown artifacts
                code = code.strip()
                if code.startswith('```python'):
                    code = code[len('```python'):].strip()
                if code.startswith('```'):
                    code = code[3:].strip()
                if code.endswith('```'):
                    code = code[:-3].strip()

        return code

    def _format_functions_for_prompt(self, functions: List[Dict[str, Any]]) -> str:
        """Format functions for LLM prompt.

        Args:
            functions: Functions to format

        Returns:
            Formatted string
        """
        parts = []
        for func in functions:
            parts.append(
                f"{func['signature']}\n"
                f"  Parameters: {', '.join(func['parameters']) if func['parameters'] else 'none'}\n"
                f"  Returns: {', '.join(func['returns']) if func['returns'] else 'none'}\n"
                f"  Purpose: {func['category']}"
            )
        return "\n\n".join(parts)
