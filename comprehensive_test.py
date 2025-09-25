#!/usr/bin/env python3
"""
Comprehensive Algorithm Comparison

Tests generalized vs traditional algorithms on multiple graph types
to ensure output equivalence across different scenarios.
"""

import sys, os
sys.path.append('.')
import time

from src import (
    generalized_mst, kruskal_mst, prim_mst,
    apsp_sssp, floyd_warshall, dijkstra,
    SHORTEST_PATH_SEMIRING,
    generate_random_mtx_file, load_mtx_as_dense_list
)

def create_test_matrix(name, n, density, description):
    """Create a test matrix and return its info."""
    filename = f"test_data/{name}.mtx"
    print(f"  Creating {description} ({n}x{n}, density={density})...")
    generate_random_mtx_file(filename, n=n, density=density, symmetric=True, pattern=False)
    return filename

def compare_algorithms(W, n, test_name):
    """Compare all algorithms on a given matrix."""
    print(f"\n{'='*50}")
    print(f"TESTING: {test_name}")
    print(f"Matrix size: {n}x{n}")
    print(f"{'='*50}")
    
    results = {}
    
    # 1. APSP Comparison
    print("🔄 ALL-PAIRS SHORTEST PATH:")
    start_time = time.time()
    gen_apsp = apsp_sssp(W, n, SHORTEST_PATH_SEMIRING)
    gen_time = (time.time() - start_time) * 1000
    
    start_time = time.time()  
    trad_apsp = floyd_warshall(W)
    trad_time = (time.time() - start_time) * 1000
    
    # Compare matrices
    apsp_match = compare_matrices(gen_apsp, trad_apsp)
    print(f"  Generalized: {gen_time:.2f}ms")
    print(f"  Traditional: {trad_time:.2f}ms")
    print(f"  Results match: {apsp_match}")
    results['apsp_match'] = apsp_match
    
    # 2. SSSP Comparison
    print("\n🎯 SINGLE-SOURCE SHORTEST PATH (source=0):")
    start_time = time.time()
    gen_sssp = apsp_sssp(W, n, SHORTEST_PATH_SEMIRING, source=0)
    gen_sssp_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    trad_sssp = dijkstra(W, 0)
    trad_sssp_time = (time.time() - start_time) * 1000
    
    # Compare vectors (gen_sssp returns matrix, take first row)
    sssp_match = compare_vectors(gen_sssp[0], trad_sssp)
    print(f"  Generalized: {gen_sssp_time:.2f}ms")
    print(f"  Traditional: {trad_sssp_time:.2f}ms")
    print(f"  Results match: {sssp_match}")
    results['sssp_match'] = sssp_match
    
    # 3. MST Comparison
    print("\n🌳 MINIMUM SPANNING TREE:")
    start_time = time.time()
    gen_mst = generalized_mst(W, n, SHORTEST_PATH_SEMIRING)
    gen_mst_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    kruskal_result = kruskal_mst(W)
    kruskal_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    prim_result = prim_mst(W)
    prim_time = (time.time() - start_time) * 1000
    
    # Compare MST total weights
    gen_weight = sum(weight for _, _, weight in gen_mst)
    kruskal_weight = sum(weight for _, _, weight in kruskal_result)
    prim_weight = sum(weight for _, _, weight in prim_result)
    
    weight_match = (abs(gen_weight - kruskal_weight) < 1e-6 and 
                   abs(gen_weight - prim_weight) < 1e-6)
    
    print(f"  Generalized: {gen_mst_time:.2f}ms, {len(gen_mst)} edges, weight={gen_weight:.2f}")
    print(f"  Kruskal:     {kruskal_time:.2f}ms, {len(kruskal_result)} edges, weight={kruskal_weight:.2f}")
    print(f"  Prim:        {prim_time:.2f}ms, {len(prim_result)} edges, weight={prim_weight:.2f}")
    print(f"  Total weights match: {weight_match}")
    results['mst_weight_match'] = weight_match
    
    return results

def compare_matrices(mat1, mat2, tolerance=1e-6):
    """Compare two matrices for equality."""
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
    """Compare two vectors for equality."""
    if len(vec1) != len(vec2):
        return False
    
    for i in range(len(vec1)):
        val1 = vec1[i] if vec1[i] != float('inf') else 999999
        val2 = vec2[i] if vec2[i] != float('inf') else 999999
        if abs(val1 - val2) > tolerance:
            return False
    return True

def main():
    print("🔬 COMPREHENSIVE GENERALIZED vs TRADITIONAL ALGORITHM COMPARISON")
    print("="*70)
    print("Testing APSP, SSSP, and MST algorithms for output equivalence")
    print("="*70)
    
    os.makedirs("test_data", exist_ok=True)
    
    # Create different types of test matrices
    print("\n📁 Creating test matrices...")
    test_matrices = [
        ("small_sparse", 5, 0.3, "Small sparse graph"),
        ("small_dense", 5, 0.8, "Small dense graph"), 
        ("medium_sparse", 8, 0.25, "Medium sparse graph"),
        ("medium_dense", 8, 0.6, "Medium dense graph"),
        ("large_sparse", 12, 0.2, "Large sparse graph"),
    ]
    
    test_files = []
    for name, n, density, desc in test_matrices:
        filename = create_test_matrix(name, n, density, desc)
        test_files.append((filename, desc))
    
    # Run comprehensive tests
    print("\n🧪 Running comprehensive algorithm comparisons...")
    all_results = {}
    successful_tests = 0
    
    for filename, description in test_files:
        try:
            W = load_mtx_as_dense_list(filename)
            n = len(W)
            results = compare_algorithms(W, n, description)
            all_results[description] = results
            successful_tests += 1
        except Exception as e:
            print(f"❌ Error testing {description}: {e}")
    
    # Final Summary
    print(f"\n{'='*70}")
    print("📊 FINAL COMPREHENSIVE SUMMARY")
    print(f"{'='*70}")
    
    print(f"✅ Successfully tested {successful_tests}/{len(test_files)} test cases")
    
    # Count matches across all tests
    apsp_successes = sum(1 for r in all_results.values() if r.get('apsp_match', False))
    sssp_successes = sum(1 for r in all_results.values() if r.get('sssp_match', False))
    mst_successes = sum(1 for r in all_results.values() if r.get('mst_weight_match', False))
    
    print(f"\n🎯 ALGORITHM EQUIVALENCE RESULTS:")
    print(f"   APSP: {apsp_successes}/{successful_tests} tests passed")
    print(f"   SSSP: {sssp_successes}/{successful_tests} tests passed") 
    print(f"   MST:  {mst_successes}/{successful_tests} tests passed")
    
    all_passed = (apsp_successes == successful_tests and 
                 sssp_successes == successful_tests and 
                 mst_successes == successful_tests)
    
    print(f"\n{'🎉' if all_passed else '⚠️'} CONCLUSION:")
    if all_passed:
        print("   ✅ ALL TESTS PASSED!")
        print("   ✅ Generalized algorithms produce identical results to traditional algorithms")
        print("   ✅ The semiring framework correctly implements graph algorithms")
        print("   ✅ APSP, SSSP, and MST all work correctly with the unified approach")
    else:
        print("   ⚠️  Some tests failed - investigation needed")
        print("   📝 Check individual test results above for details")
if __name__ == "__main__":
    main()
