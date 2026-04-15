#!/usr/bin/env python3
"""
Test runner script for Field Network Checker.
Runs pytest and reports results.
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run the test suite and return exit code."""
    test_dir = Path(__file__).parent / "tests"
    if not test_dir.exists():
        print("No tests directory found.")
        return 1

    cmd = [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode
    except FileNotFoundError:
        print("pytest not installed. Run: pip install pytest pytest-mock")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())