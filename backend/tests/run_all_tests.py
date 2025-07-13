#!/usr/bin/env python3
"""
Test runner script for all backend unit tests
"""

import unittest
import sys
import os
from pathlib import Path

# Add the backend src directory to Python path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(src_dir))

def run_all_tests():
    """Discover and run all unit tests"""
    
    # Test discovery
    loader = unittest.TestLoader()
    test_dir = Path(__file__).parent
    
    # Discover all test files
    suite = loader.discover(
        start_dir=str(test_dir),
        pattern='test_*_unittest.py',
        top_level_dir=str(backend_dir)
    )
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    print("=" * 70)
    print("Running Backend Unit Tests")
    print("=" * 70)
    
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

def run_specific_test_module(module_name):
    """Run tests from a specific module"""
    
    try:
        # Import the test module
        test_module = __import__(f"tests.{module_name}", fromlist=[module_name])
        
        # Create test suite from module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
        
    except ImportError as e:
        print(f"Error importing test module '{module_name}': {e}")
        return 1

def list_available_tests():
    """List all available test modules"""
    
    test_dir = Path(__file__).parent
    test_files = list(test_dir.glob("test_*_unittest.py"))
    
    print("Available test modules:")
    for test_file in sorted(test_files):
        module_name = test_file.stem
        print(f"  - {module_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_available_tests()
            sys.exit(0)
        elif command.startswith("test_"):
            # Run specific test module
            exit_code = run_specific_test_module(command)
            sys.exit(exit_code)
        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python run_all_tests.py           # Run all tests")
            print("  python run_all_tests.py list      # List available tests")
            print("  python run_all_tests.py test_*    # Run specific test module")
            sys.exit(1)
    else:
        # Run all tests
        exit_code = run_all_tests()
        sys.exit(exit_code)