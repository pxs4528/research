#!/usr/bin/env python3
"""
Simple MST Comparison Test
"""

import sys, os
sys.path.append('.')

from src import (
    generalized_mst, kruskal_mst, prim_mst,
    apsp_sssp, floyd_warshall, dijkstra,
    SHORTEST_PATH_SEMIRING,
    generate_random_mtx_file, load_mtx_as_dense_list
)

def test_algorithms():
    print("🔬 TESTING GENERALIZED vs TRADITIONAL ALGORITHMS")
    print("="*60)
    
    # Generate a test matrix
    print("📁 Generating test matrix...")
    generate_random_mtx_file("test_data/simple_test.mtx", n=5, density=0.6, 
                           symmetric=True, pattern=False)
    
    # Load matrix
    W = load_mtx_as_dense_list("test_data/simple_test.mtx")
    n = len(W)
    print(f"Matrix size: {n}x{n}")
    
    print("\n📊 ALGORITHM RESULTS:")
    print("-" * 40)
    
    # Test APSP
    print("🔄 ALL-PAIRS SHORTEST PATH:")
    gen_apsp = apsp_sssp(W, n, SHORTEST_PATH_SEMIRING)
    trad_apsp = floyd_warshall(W)
    
    # Compare a few values
    apsp_match = True
    for i in range(min(3, n)):
        for j in range(min(3, n)):
            val1 = gen_apsp[i][j] if gen_apsp[i][j] != float('inf') else 999
            val2 = trad_apsp[i][j] if trad_apsp[i][j] != float('inf') else 999
            if abs(val1 - val2) > 1e-6:
                apsp_match = False
                break
        if not apsp_match:
            break
    
    print(f"  Generalized vs Traditional APSP match: {apsp_match}")
    
    # Test SSSP
    print("\n🎯 SINGLE-SOURCE SHORTEST PATH (source=0):")
    gen_sssp = apsp_sssp(W, n, SHORTEST_PATH_SEMIRING, source=0)
    trad_sssp = dijkstra(W, 0)
    
    sssp_match = True
    for i in range(n):
        val1 = gen_sssp[0][i] if gen_sssp[0][i] != float('inf') else 999
        val2 = trad_sssp[i] if trad_sssp[i] != float('inf') else 999
        if abs(val1 - val2) > 1e-6:
            sssp_match = False
            break
    
    print(f"  Generalized vs Traditional SSSP match: {sssp_match}")
    
    # Test MST
    print("\n🌳 MINIMUM SPANNING TREE:")
    gen_mst = generalized_mst(W, n, SHORTEST_PATH_SEMIRING)
    kruskal_mst_result = kruskal_mst(W)
    prim_mst_result = prim_mst(W)
    
    print(f"  Generalized MST: {len(gen_mst)} edges")
    print(f"  Kruskal MST:     {len(kruskal_mst_result)} edges")
    print(f"  Prim MST:        {len(prim_mst_result)} edges")
    
    # For MST, check if total weights are equal (MSTs might have different edge sets but same total weight)
    def total_weight(edges):
        return sum(weight for _, _, weight in edges)
    
    gen_weight = total_weight(gen_mst)
    kruskal_weight = total_weight(kruskal_mst_result)
    prim_weight = total_weight(prim_mst_result)
    
    print(f"  Total weights - Gen: {gen_weight:.2f}, Kruskal: {kruskal_weight:.2f}, Prim: {prim_weight:.2f}")
    
    weight_match = (abs(gen_weight - kruskal_weight) < 1e-6 and 
                   abs(gen_weight - prim_weight) < 1e-6)
    print(f"  MST total weights match: {weight_match}")
    
    # Display actual edges for small graphs
    if n <= 5:
        print(f"\n📋 MST EDGE DETAILS:")
        print(f"  Generalized: {gen_mst}")
        print(f"  Kruskal:     {kruskal_mst_result}")
        print(f"  Prim:        {prim_mst_result}")
    
    print("\n" + "="*60)
    print("📊 SUMMARY:")
    print(f"  ✅ APSP algorithms match: {apsp_match}")
    print(f"  ✅ SSSP algorithms match: {sssp_match}")
    print(f"  ✅ MST total weights match: {weight_match}")
    
    if apsp_match and sssp_match and weight_match:
        print("\n🎉 SUCCESS: All generalized algorithms produce equivalent results!")
    else:
        print("\n⚠️  Some algorithms don't match - further investigation needed")

if __name__ == "__main__":
    os.makedirs("test_data", exist_ok=True)
    test_algorithms()
