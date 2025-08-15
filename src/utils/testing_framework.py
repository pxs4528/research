"""
Algorithm testing framework.

This module provides a framework for testing and comparing different
graph algorithms on Matrix Market files.
"""

import os
from typing import List, Callable, Dict, Any
from src.core.semiring import Semiring, SHORTEST_PATH_SEMIRING
from src.utils.matrix_utils import load_mtx_as_dense_list, find_mtx_files


class AlgorithmTester:
    """Class to manage and run algorithm tests on multiple files."""
    
    def __init__(self, semiring: Semiring = None):
        """Initialize the tester with a default semiring."""
        self.semiring = semiring or SHORTEST_PATH_SEMIRING
        self.results = {}
        self.algorithms = []
    
    def add_algorithm(self, name: str, func: Callable, **kwargs):
        """Add an algorithm to test."""
        self.algorithms.append((func, name, kwargs))
    
    def run_single_test(self, algorithm_func: Callable, W: List[List[float]], n: int, 
                       algorithm_name: str, **kwargs) -> List[List[float]]:
        """Run a single algorithm test and return results."""
        print(f"  Running {algorithm_name}...")
        try:
            result = algorithm_func(W, n, self.semiring, **kwargs)
            print(f"  ✓ {algorithm_name} completed successfully")
            return result
        except Exception as e:
            print(f"  ✗ Error in {algorithm_name}: {e}")
            return []
    
    def test_file(self, file_path: str) -> Dict[str, Any]:
        """Test all algorithms on a single Matrix Market file."""
        print(f"\n{'='*60}")
        print(f"Testing file: {os.path.basename(file_path)}")
        print(f"{'='*60}")
        
        try:
            W = load_mtx_as_dense_list(file_path)
            if not W:
                print("Warning: Empty matrix loaded")
                return {}
                
            n = len(W)
            print(f"Matrix size: {n}x{n}")
            
            # Default algorithms if none specified
            if not self.algorithms:
                from src.algorithms.generalized import apsp_sssp, slow_apsp
                self.algorithms = [
                    (apsp_sssp, "Generalized APSP/SSSP", {}),
                    (slow_apsp, "Slow APSP", {}),
                    (apsp_sssp, "SSSP from node 0", {"source": 0})
                ]
            
            file_results = {}
            for algo_func, algo_name, kwargs in self.algorithms:
                result = self.run_single_test(algo_func, W, n, algo_name, **kwargs)
                file_results[algo_name] = result
                
            self.results[file_path] = file_results
            return file_results
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return {}
    
    def display_results(self, max_display_size: int = 10, max_rows_to_show: int = 5):
        """Display test results in a formatted way."""
        print(f"\n{'='*80}")
        print("RESULTS SUMMARY")
        print(f"{'='*80}")
        
        for file_path, file_results in self.results.items():
            print(f"\nFile: {os.path.basename(file_path)}")
            print("-" * 40)
            
            for algo_name, result in file_results.items():
                if not result:
                    print(f"{algo_name}: FAILED")
                    continue
                    
                print(f"\n{algo_name}:")
                if len(result) <= max_display_size:
                    for i, row in enumerate(result[:max_rows_to_show]):
                        formatted_row = [f"{x:.2f}" if x != float('inf') else "∞" for x in row[:max_rows_to_show]]
                        print(f"  Row {i}: {formatted_row}{'...' if len(row) > max_rows_to_show else ''}")
                    if len(result) > max_rows_to_show:
                        print("  ...")
                else:
                    print(f"  [Matrix too large to display - size: {len(result)}x{len(result[0]) if result else 0}]")
    
    def run_tests(self, directory: str = ".", generate_if_empty: bool = True) -> Dict[str, Any]:
        """Run tests on all Matrix Market files in the specified directory."""
        print("Algorithm Testing Framework")
        print("="*40)
        
        # Find test files
        mtx_files = find_mtx_files(directory)
        if not mtx_files and generate_if_empty:
            print("No .mtx files found. Generating test file...")
            from ..utils.matrix_utils import generate_random_mtx_file
            generate_random_mtx_file("test_graph.mtx", n=5, density=0.3, symmetric=True)
            mtx_files = find_mtx_files(directory)
        
        if not mtx_files:
            print("No Matrix Market files found to test.")
            return {}
        
        print(f"Found {len(mtx_files)} file(s) to test: {[os.path.basename(f) for f in mtx_files]}")
        
        # Test algorithms on all found files
        for file_path in mtx_files:
            self.test_file(file_path)
        
        print(f"\nTesting completed on {len(mtx_files)} file(s).")
        return self.results
