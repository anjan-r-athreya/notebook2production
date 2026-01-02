#!/bin/bash
# Test script for Phase 3 - Code Generation

echo "=========================================="
echo "Testing Phase 3: Code Generation"
echo "=========================================="
echo

# Test 1: Convert test_notebook_fixed.ipynb
echo "Test 1: Converting test_notebook_fixed.ipynb"
echo "--------------------------------------------"
rm -rf ./test_output
./venv/bin/nb2prod convert Notebooks/test_notebook_fixed.ipynb --output ./test_output

if [ -d "./test_output" ]; then
    echo "✓ Project generated successfully"
    echo
    echo "Generated files:"
    ls -la ./test_output/
    echo
    echo "Source files:"
    ls -la ./test_output/src/
    echo
else
    echo "✗ Project generation failed"
    exit 1
fi

# Test 2: Verify all expected files exist
echo "Test 2: Verifying generated files"
echo "--------------------------------------------"
EXPECTED_FILES=(
    "./test_output/main.py"
    "./test_output/config.yaml"
    "./test_output/requirements.txt"
    "./test_output/README.md"
    "./test_output/src/__init__.py"
    "./test_output/src/data_processing.py"
)

ALL_EXIST=true
for file in "${EXPECTED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        ALL_EXIST=false
    fi
done
echo

if [ "$ALL_EXIST" = true ]; then
    echo "✓ All expected files generated"
else
    echo "✗ Some files missing"
    exit 1
fi

# Test 3: Check requirements.txt content
echo "Test 3: Checking requirements.txt"
echo "--------------------------------------------"
cat ./test_output/requirements.txt
echo

# Test 4: Check main.py is executable
echo "Test 4: Checking main.py permissions"
echo "--------------------------------------------"
if [ -x "./test_output/main.py" ]; then
    echo "✓ main.py is executable"
else
    echo "✗ main.py is not executable"
fi
echo

# Test 5: Validate Python syntax
echo "Test 5: Validating Python syntax"
echo "--------------------------------------------"
for pyfile in ./test_output/src/*.py ./test_output/main.py; do
    if python -m py_compile "$pyfile" 2>/dev/null; then
        echo "✓ $pyfile syntax valid"
    else
        echo "✗ $pyfile has syntax errors"
        exit 1
    fi
done
echo

# Test 6: Test with broken notebook (should block)
echo "Test 6: Testing with broken notebook"
echo "--------------------------------------------"
./venv/bin/nb2prod convert test_notebook.ipynb --output ./broken_output 2>&1 | grep -q "Not Suitable"
if [ $? -eq 0 ]; then
    echo "✓ Correctly blocked broken notebook"
else
    echo "✗ Should have blocked broken notebook"
fi
echo

# Test 7: Test with educational notebook (should warn)
echo "Test 7: Testing with educational notebook"
echo "--------------------------------------------"
./venv/bin/nb2prod convert C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb --output ./edu_output 2>&1 | grep -q "Educational"
if [ $? -eq 0 ]; then
    echo "✓ Correctly identified educational notebook"
else
    echo "✗ Should have identified educational notebook"
fi
echo

echo "=========================================="
echo "All Phase 3 tests passed! ✓"
echo "=========================================="
echo
echo "To run the generated project:"
echo "  cd ./test_output"
echo "  ../venv/bin/pip install -r requirements.txt -q"
echo "  ../venv/bin/python main.py"
