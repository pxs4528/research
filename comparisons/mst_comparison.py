#!/usr/bin/env python3
"""
MST Comparison: Generalized vs Traditional

This script specifically compares generalized MST with traditional MST algorithms
to verify they produce the same output.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from src import (
    SHORTEST_PATH_SEMIRING, apsp_sssp, generalized_mst,
    floyd_warshall, dijkstra, kruskal_mst, prim_mst,
    load_mtx_as_dense_list, generate_random_mtx_file
)


def time_algorithm(func, *args, **kwargs):
    """Time an algorithm execution and return result with timing info."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, (end_time - start_time) * 1000


def normalize_mst_edges(edges):
    """Normalize MST edges for comparison by sorting."""
    normalized = []
    for u, v, weight in edges:
        # Ensure smaller vertex comes first
        if u > v:
            u, v = v, u
        normalized.append((u, v, weight))
    
    # Sort by weight, then by vertices
    normalized.sort(key=lambda x: (x[2], x[0], x[1]))
    return normalized


def compare_mst_results(edges1, edges2, tolerance=1e-6):
    """Compare two MST edge lists for equivalence."""
    norm1 = normalize_mst_edges(edges1)
    norm2 = normalize_mst_edges(edges2)
    
    if len(norm1) != len(norm2):
        return False
    
    for (u1, v1, w1), (u2, v2, w2) in zip(norm1, norm2):
        if u1 != u2 or v1 != v2 or abs(w1 - w2) > tolerance:
            return False
    
    return True


def format_mst_edges(edges, max_edges=5):
    """Format MST edges for display."""
    if not edges:
        return "No edges"
    
    formatted = []
    total_weight = 0
    display_edges = edges[:max_edges]
    
    for u, v, weight in display_edges:
        formatted.append(f"({u}-{v}:{weight:.1f})")
        total_weight += weight
    
    # Add total weight from all edges
    for u, v, weight in edges:
        if (u, v, weight) not in display_edges:
            total_weight += weight
    
    result = f"[{', '.join(formatted)}"
    if len(edges) > max_edges:
        result += f", +{len(edges)-max_edges} more"
    result += f"] Total: {total_weight:.1f}"
    
    return result


def compare_algorithms_on_file(file_path: str):
    """Compare all algorithms on a single file."""
    print(f"\n{'='*70}")
    print(f"COMPARING ALGORITHMS ON: {os.path.basename(file_path)}")
    print(f"{'='*70}")
    
    try:
        # Load the matrix
        W = load_mtx_as_dense_list(file_path)
        n = len(W)
        print(f"Matrix size: {n}x{n}")
        
        print(f"\n📊 ALGORITHM COMPARISON RESULTS:")
        print("-" * 50)
        
        # 1. All-Pairs Shortest Path Comparison
        print(f"🔄 ALL-PAIRS SHORTEST PATH (APSP):")
        
        result_gen, time_gen = time_algorithm(apsp_sssp, W, n, SHORTEST_PATH_SEMIRING)
        print(f"  ⚡ Generalized (Semiring):     {time_gen:.2f}ms")
        
        result_trad, time_trad = time_algorithm(floyd_warshall, W)
        print(f"  🔧 Traditional (Floyd-Warshall): {time_trad:.2f}ms")
        
        apsp_match = compare_matrices(result_gen, result_trad)
        print(f"  ✅ Results match: {apsp_match}")
        
        # 2. Single-Source Shortest Path Comparison
        print(f"\n🎯 SINGLE-SOURCE SHORTEST PATH (SSSP) from node 0:")
        
        result_gen_sssp, time_gen_sssp = time_algorithm(apsp_sssp, W, n, SHORTEST_PATH_SEMIRING, source=0)
        print(f"  ⚡ Generalized (Semiring):  {time_gen_sssp:.2f}ms")
        
        result_trad_sssp, time_trad_sssp = time_algorithm(dijkstra, W, 0)
        print(f"  🔧 Traditional (Dijkstra):   {time_trad_sssp:.2f}ms")
        
        sssp_match = compare_vectors(result_gen_sssp[0], result_trad_sssp)
        print(f"  ✅ Results match: {sssp_match}")
        
        # 3. Minimum Spanning Tree Comparison
        print(f"\n🌳 MINIMUM SPANNING TREE (MST):")
        
        result_gen_mst, time_gen_mst = time_algorithm(generalized_mst, W, n, SHORTEST_PATH_SEMIRING)
        print(f"  ⚡ Generalized (Semiring):  {time_gen_mst:.2f}ms - {len(result_gen_mst)} edges")
        
        result_kruskal, time_kruskal = time_algorithm(kruskal_mst, W)
        print(f"  🌳 Traditional (Kruskal):   {time_kruskal:.2f}ms - {len(result_kruskal)} edges")
        
        result_prim, time_prim = time_algorithm(prim_mst, W)
        print(f"  🌿 Traditional (Prim):      {time_prim:.2f}ms - {len(result_prim)} edges")
        
        # Compare MST results
        mst_gen_vs_kruskal = compare_mst_results(result_gen_mst, result_kruskal)
        mst_gen_vs_prim = compare_mst_results(result_gen_mst, result_prim)
        mst_kruskal_vs_prim = compare_mst_results(result_kruskal, result_prim)
        
        print(f"  ✅ Generalized ≡ Kruskal: {mst_gen_vs_kruskal}")
        print(f"  ✅ Generalized ≡ Prim:    {mst_gen_vs_prim}")
        print(f"  ✅ Kruskal ≡ Prim:        {mst_kruskal_vs_prim}")
        
        # Display sample results for smaller matrices
        if n <= 6:
            print(f"\n📋 DETAILED RESULTS:")
            print(f"  APSP - Gen vs Trad match:  {apsp_match}")
            print(f"  SSSP - Gen vs Trad match:  {sssp_match}")
            print(f"  MST Edges - Generalized:   {format_mst_edges(result_gen_mst)}")
            print(f"  MST Edges - Kruskal:       {format_mst_edges(result_kruskal)}")
            print(f"  MST Edges - Prim:          {format_mst_edges(result_prim)}")
        
        return {
            'apsp_match': apsp_match,
            'sssp_match': sssp_match,
            'mst_gen_vs_kruskal': mst_gen_vs_kruskal,
            'mst_gen_vs_prim': mst_gen_vs_prim,
            'mst_algorithms_consistent': mst_kruskal_vs_prim
        }
        
    except Exception as e:
        print(f"❌ Error in comparison: {e}")
        import traceback
        traceback.print_exc()
        return {}


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


def main():
    """Main comparison function."""
    print("🔬 GENERALIZED vs TRADITIONAL ALGORITHMS COMPARISON")
    print("   Including APSP, SSSP, and MST algorithms")
    print("="*70)
    
    # Generate test files for comparison
    print("\n📁 Generating test matrices...")
    os.makedirs("test_data", exist_ok=True)
    
    # Generate weighted graphs suitable for MST
    generate_random_mtx_file("test_data/mst_small.mtx", n=5, density=0.6, 
                           symmetric=True, min_weight=1, max_weight=10)
    generate_random_mtx_file("test_data/mst_medium.mtx", n=7, density=0.5, 
                           symmetric=True, min_weight=1, max_weight=15)
    generate_random_mtx_file("test_data/mst_large.mtx", n=10, density=0.4, 
                           symmetric=True, min_weight=1, max_weight=20)
    
    # Test files
    test_files = [
        "test_data/mst_small.mtx",
        "test_data/mst_medium.mtx", 
        "test_data/mst_large.mtx"
    ]
    
    # Add existing comparison files if they exist
    existing_files = [
        "test_data/comparison_small.mtx",
        "test_data/comparison_medium.mtx"
    ]
    
    for file_path in existing_files:
        if os.path.exists(file_path):
            test_files.append(file_path)
    
    # Run comparisons
    all_results = {}
    successful_tests = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            results = compare_algorithms_on_file(file_path)
            if results:
                all_results[file_path] = results
                successful_tests += 1
        else:
            print(f"⚠️  File {file_path} not found, skipping...")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 COMPREHENSIVE COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Successfully tested {successful_tests} files")
    
    # Count successful matches
    apsp_matches = sum(1 for r in all_results.values() if r.get('apsp_match', False))
    sssp_matches = sum(1 for r in all_results.values() if r.get('sssp_match', False))
    mst_gen_kruskal_matches = sum(1 for r in all_results.values() if r.get('mst_gen_vs_kruskal', False))
    mst_gen_prim_matches = sum(1 for r in all_results.values() if r.get('mst_gen_vs_prim', False))
    
    print(f"\n🎯 ALGORITHM CORRECTNESS:")
    print(f"   APSP: Generalized ≡ Traditional in {apsp_matches}/{successful_tests} tests")
    print(f"   SSSP: Generalized ≡ Traditional in {sssp_matches}/{successful_tests} tests")
    print(f"   MST:  Generalized ≡ Kruskal in {mst_gen_kruskal_matches}/{successful_tests} tests")
    print(f"   MST:  Generalized ≡ Prim in {mst_gen_prim_matches}/{successful_tests} tests")
    
    print(f"\n📈 KEY FINDINGS:")
    if all(r.get('apsp_match', False) for r in all_results.values()):
        print(f"   ✅ Generalized APSP produces identical results to Floyd-Warshall")
    else:
        print(f"   ⚠️  Some APSP results don't match - needs investigation")
        
    if all(r.get('sssp_match', False) for r in all_results.values()):
        print(f"   ✅ Generalized SSSP produces identical results to Dijkstra")
    else:
        print(f"   ⚠️  Some SSSP results don't match - needs investigation")
        
    if all(r.get('mst_gen_vs_kruskal', False) and r.get('mst_gen_vs_prim', False) 
           for r in all_results.values()):
        print(f"   ✅ Generalized MST produces identical results to traditional MST")
    else:
        print(f"   ⚠️  Some MST results don't match - needs investigation")
    
    print(f"\n🔬 SEMIRING FRAMEWORK VALIDATION:")
    print(f"   • The generalized algorithms use semiring operations")
    print(f"   • SHORTEST_PATH_SEMIRING = (min, +, ∞, 0)")
    print(f"   • This should be mathematically equivalent to traditional approaches")
    print(f"   • Identical outputs confirm the correctness of the generalized approach")


if __name__ == "__main__":
    main()
