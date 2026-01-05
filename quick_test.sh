#!/bin/bash
echo "=== Phase 5 Verification Test ==="
echo ""

echo "1. Testing CLI Help..."
nb2prod --help > /dev/null && echo "   ✅ CLI works" || echo "   ❌ CLI failed"

echo "2. Running Test Suite..."
pytest tests/ -q && echo "   ✅ All tests pass" || echo "   ❌ Tests failed"

echo "3. Testing Analyze Command..."
nb2prod analyze Notebooks/customer_churn_prediction.ipynb > /dev/null 2>&1 && echo "   ✅ Analyze works" || echo "   ❌ Analyze failed"

echo "4. Testing Convert Command..."
nb2prod convert Notebooks/customer_churn_prediction.ipynb -o ./phase5_test > /dev/null 2>&1 && echo "   ✅ Convert works" || echo "   ❌ Convert failed"

echo "5. Checking Generated Project..."
if [ -d "./phase5_test" ]; then
    echo "   ✅ Project directory created"
    [ -f "./phase5_test/main.py" ] && echo "   ✅ main.py exists" || echo "   ❌ main.py missing"
    [ -f "./phase5_test/README.md" ] && echo "   ✅ README.md exists" || echo "   ❌ README.md missing"
    [ -d "./phase5_test/src" ] && echo "   ✅ src/ directory exists" || echo "   ❌ src/ missing"
else
    echo "   ❌ Project directory not created"
fi

echo ""
echo "=== Verification Complete ==="
