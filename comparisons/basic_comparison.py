#!/usr/bin/env python3
"""
Basic Comparison: Generalized vs Traditional Graph Algorithms

This demonstrates the difference between generalized semiring-based algorithms
and traditional graph algorithms using the testing framework.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from src import (
    SHORTEST_PATH_SEMIRING, apsp_sssp, slow_apsp,
    floyd_warshall, dijkstra,
    load_mtx_as_dense_list, generate_random_mtx_file
)


def time_algorithm(func, *args, **kwargs):
    """Time an algorithm execution and return result with timing info."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, (end_time - start_time) * 1000  # Return time in milliseconds


def compare_algorithms_on_file(file_path: str):
    """Compare generalized vs traditional algorithms on a single file."""
    print(f"\n{'='*70}")
    print(f"COMPARING ALGORITHMS ON: {os.path.basename(file_path)}")
    print(f"{'='*70}")
    
    try:
        # Load the matrix
        W = load_mtx_as_dense_list(file_path)
        n = len(W)
        print(f"Matrix size: {n}x{n}")
        
        print(f"\n ALGORITHM COMPARISON RESULTS:")
        print("-" * 50)
        
        # 1. All-Pairs Shortest Path Comparison
        print(f"\n ALL-PAIRS SHORTEST PATH (APSP):")
        
        # Generalized approach
        result_gen, time_gen = time_algorithm(apsp_sssp, W, n, SHORTEST_PATH_SEMIRING)
        print(f"   Generalized (Semiring):     {time_gen:.2f}ms")
        
        # Traditional approach
        result_trad, time_trad = time_algorithm(floyd_warshall, W)
        print(f"   Traditional (Floyd-Warshall): {time_trad:.2f}ms")
        
        # Slow approach for comparison
        result_slow, time_slow = time_algorithm(slow_apsp, W, n, SHORTEST_PATH_SEMIRING)
        print(f"   Slow APSP (Matrix Powers):   {time_slow:.2f}ms")
        
        # Check if results are equivalent
        results_match = compare_matrices(result_gen, result_trad)
        print(f"   Results match: {results_match}")
        
        # Performance comparison
        if time_trad > 0:
            speedup = time_trad / time_gen if time_gen > 0 else float('inf')
            print(f"   Traditional vs Generalized: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")
        
        # 2. Single-Source Shortest Path Comparison
        print(f"\n SINGLE-SOURCE SHORTEST PATH (SSSP) from node 0:")
        
        # Generalized approach
        result_gen_sssp, time_gen_sssp = time_algorithm(apsp_sssp, W, n, SHORTEST_PATH_SEMIRING, source=0)
        print(f"   Generalized (Semiring):  {time_gen_sssp:.2f}ms")
        
        # Traditional approach
        result_trad_sssp, time_trad_sssp = time_algorithm(dijkstra, W, 0)
        print(f"   Traditional (Dijkstra):   {time_trad_sssp:.2f}ms")
        
        # Check if results are equivalent
        sssp_match = compare_vectors(result_gen_sssp[0], result_trad_sssp)
        print(f"   Results match: {sssp_match}")
        
        # Performance comparison
        if time_trad_sssp > 0:
            sssp_speedup = time_trad_sssp / time_gen_sssp if time_gen_sssp > 0 else float('inf')
            print(f"   Traditional vs Generalized: {sssp_speedup:.2f}x {'faster' if sssp_speedup > 1 else 'slower'}")
        
        # Display small results for verification
        if n <= 6:
            print(f"\n SAMPLE RESULTS (first 3 rows/elements):")
            print(f"  APSP - Generalized:  {format_matrix_sample(result_gen, 3)}")
            print(f"  APSP - Traditional:  {format_matrix_sample(result_trad, 3)}")
            print(f"  SSSP - Generalized:  {format_vector_sample(result_gen_sssp[0], 6)}")
            print(f"  SSSP - Traditional:  {format_vector_sample(result_trad_sssp, 6)}")
        
    except Exception as e:
        print(f"Error in comparison: {e}")


def compare_matrices(mat1, mat2, tolerance=1e-6):
    """Compare two matrices for equality within tolerance."""
    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        return False
    
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            val1 = mat1[i][j] if mat1[i][j] != float('inf') else 999999
            val2 = mat2[i][j] if mat2[i][j] != float('inf') else 999999
            if abs(val1 - val2) > tolerance:
                return False
    return True


def compare_vectors(vec1, vec2, tolerance=1e-6):
    """Compare two vectors for equality within tolerance."""
    if len(vec1) != len(vec2):
        return False
    
    for i in range(len(vec1)):
        val1 = vec1[i] if vec1[i] != float('inf') else 999999
        val2 = vec2[i] if vec2[i] != float('inf') else 999999
        if abs(val1 - val2) > tolerance:
            return False
    return True


def format_matrix_sample(matrix, max_rows=3):
    """Format a sample of matrix for display."""
    sample = []
    for i in range(min(len(matrix), max_rows)):
        row = [f"{x:.1f}" if x != float('inf') else "∞" for x in matrix[i][:max_rows]]
        sample.append(f"[{', '.join(row)}{'...' if len(matrix[i]) > max_rows else ''}]")
    return f"[{', '.join(sample)}{'...' if len(matrix) > max_rows else ''}]"


def format_vector_sample(vector, max_elements=6):
    """Format a sample of vector for display."""
    elements = [f"{x:.1f}" if x != float('inf') else "∞" for x in vector[:max_elements]]
    return f"[{', '.join(elements)}{'...' if len(vector) > max_elements else ''}]"


def main():
    """Main comparison function."""
    print(" GENERALIZED vs TRADITIONAL ALGORITHMS COMPARISON")
    print("="*60)
    
    # Generate some test files for comparison
    print("\n Generating test matrices...")
    os.makedirs("test_data", exist_ok=True)
    
    generate_random_mtx_file("test_data/comparison_small.mtx", n=5, density=0.4, symmetric=True)
    generate_random_mtx_file("test_data/comparison_medium.mtx", n=8, density=0.3, symmetric=True)
    generate_random_mtx_file("test_data/comparison_large.mtx", n=12, density=0.25, symmetric=True)
    
    # List of test files to compare
    test_files = [
        "test_data/comparison_small.mtx",
        "test_data/comparison_medium.mtx", 
        "test_data/comparison_large.mtx"
    ]
    
    # Add existing files if they exist
    if os.path.exists("A2.mtx"):
        test_files.append("A2.mtx")
    if os.path.exists("test_small.mtx"):
        test_files.append("test_small.mtx")
    
    # Run comparisons on each file
    overall_results = {}
    for file_path in test_files:
        if os.path.exists(file_path):
            compare_algorithms_on_file(file_path)
            overall_results[file_path] = "Completed"
        else:
            print(f"⚠️  File {file_path} not found, skipping...")


if __name__ == "__main__":
    main()
