# Implementation Phases

## Phase 1: Foundation (COMPLETED ✓)
- CLI with `analyze` command
- Notebook parsing with nbformat
- AST-based cell analysis
- Dependency detection

## Phase 2: Function Extraction (NEXT)
Files to create:
- nb2prod/extractor.py
- nb2prod/grouper.py

Tasks:
1. Group related cells based on:
   - Variable dependencies
   - Cell categories (data, model, etc.)
   - Logical flow
2. Generate function signatures
3. Extract parameters from dependencies

## Phase 3: Code Generation
Files to create:
- nb2prod/generator.py
- nb2prod/templates/ (jinja2 files)

Tasks:
1. Generate src/ modules
2. Generate config.yaml
3. Generate main.py CLI
4. Generate requirements.txt

## Phase 4: LLM Enhancement
Files to create:
- nb2prod/llm_refactor.py

Tasks:
1. Send cell groups to Claude API
2. Get smart function names/signatures
3. Generate docstrings
4. Improve code quality

## Phase 5: Polish
- Test generation
- Error handling
- Documentation
- Packaging
```
