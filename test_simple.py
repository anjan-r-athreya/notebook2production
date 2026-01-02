"""Simple test without imports - just verify files exist."""
import sys
import os
from pathlib import Path

# Get the directory where this script is located
current_dir = Path(__file__).parent

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print(f"Script directory: {current_dir}")
print(f"Script directory exists: {current_dir.exists()}")
print(f"\nFiles in {current_dir}:")
if current_dir.exists():
    for f in current_dir.iterdir():
        if f.is_file():
            print(f"  - {f.name}")

# Try to import
sys.path.insert(0, str(current_dir))
try:
    import parser
    print("\n✓ Successfully imported parser module!")
    print(f"  Parser location: {parser.__file__}")
except Exception as e:
    print(f"\n✗ Failed to import: {e}")
