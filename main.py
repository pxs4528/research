#!/usr/bin/env python3
"""
Main entry point for algorithm testing and comparison.

This script provides a simple interface to run different types of
algorithm comparisons and tests.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import AlgorithmTester, apsp_sssp, slow_apsp, SHORTEST_PATH_SEMIRING


def run_basic_tests():
    """Run basic algorithm tests."""
    print(" BASIC ALGORITHM TESTING")
    print("=" * 50)
    
    # Create a tester instance
    tester = AlgorithmTester()
    
    # Run tests on all Matrix Market files in test_data directory
    results = tester.run_tests("test_data", generate_if_empty=True)
    
    # Display results
    if results:
        tester.display_results()
    else:
        print("No tests were run. Make sure you have .mtx files in the test_data directory.")


def run_comparisons():
    """Run detailed algorithm comparisons."""
    print("\n🔬 RUNNING DETAILED COMPARISONS")
    print("=" * 50)
    
    comparison_scripts = [
        ("Basic Comparison", "comparisons/basic_comparison.py"),
        ("Detailed Analysis", "comparisons/detailed_comparison.py"), 
        ("Code Structure", "comparisons/code_comparison.py")
    ]
    
    for name, script_path in comparison_scripts:
        if os.path.exists(script_path):
            print(f"\n▶ Running {name}...")
            print(f"   Script: {script_path}")
            print(f"   Run with: python {script_path}")
        else:
            print(f"  {name} script not found at {script_path}")



def main():
    """Main function."""
    print(" GRAPH ALGORITHMS RESEARCH PROJECT")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            run_basic_tests()
        elif command == "compare":
            run_comparisons()
        else:
            print(f"Unknown command: {command}")
            print_usage()
    else:
        # Default: show structure and available commands
        print_usage()
        
        # Run basic tests by default
        print("\n" + "=" * 60)
        run_basic_tests()


def print_usage():
    """Print usage information."""
    print("\n USAGE:")
    print("   python main.py test      - Run basic algorithm tests")
    print("   python main.py compare   - Show available comparison scripts")  
    print("   python main.py structure - Show project structure")
    print("   python main.py          - Show structure and run basic tests")
    
    print("\n COMPARISON SCRIPTS:")
    print("   python comparisons/basic_comparison.py      - Basic comparison")
    print("   python comparisons/detailed_comparison.py   - Detailed analysis") 
    print("   python comparisons/code_comparison.py       - Code structure comparison")


if __name__ == "__main__":
    main()
