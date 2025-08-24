#!/usr/bin/env python3
"""
Test runner script for the raw pipeline
"""
import sys
import subprocess
import os


def run_tests(test_type="unit"):
    """Run tests based on type"""
    os.chdir(os.path.dirname(__file__))
    
    if test_type == "unit":
        # Run only unit tests (exclude integration tests)
        cmd = ["python", "-m", "pytest", "-m", "not integration"]
    elif test_type == "integration":
        # Run only integration tests
        cmd = ["python", "-m", "pytest", "-m", "integration"]
    elif test_type == "all":
        # Run all tests
        cmd = ["python", "-m", "pytest"]
    else:
        print(f"Unknown test type: {test_type}")
        print("Available types: unit, integration, all")
        return 1
    
    print(f"Running {test_type} tests...")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    test_type = sys.argv[1] if len(sys.argv) > 1 else "unit"
    return run_tests(test_type)


if __name__ == "__main__":
    sys.exit(main())