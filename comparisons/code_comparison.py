#!/usr/bin/env python3
"""
Code Structure Comparison: Generalized vs Traditional

This script demonstrates the code structure differences between
generalized semiring-based and traditional algorithm implementations.
"""

def print_code_comparison():
    """Print side-by-side code comparison."""
    
    print("📝 CODE STRUCTURE COMPARISON")
    print("="*80)
    
    print(f"""
🎯 PROBLEM: All-Pairs Shortest Path (APSP)

┌─────────────────────────────────────┬─────────────────────────────────────┐
│ GENERALIZED (Semiring-based)        │ TRADITIONAL (Floyd-Warshall)       │
├─────────────────────────────────────┼─────────────────────────────────────┤
│                                     │                                     │
│ # Define the semiring structure     │ # Direct algorithm implementation   │
│ semiring = Semiring(                │ def floyd_warshall(matrix):         │
│     add=min,                        │     n = len(matrix)                 │
│     multiply=lambda x,y: x + y,     │     dist = copy.deepcopy(matrix)    │
│     zero=float('inf'),              │                                     │
│     one=0                           │     for k in range(n):              │
│ )                                   │         for i in range(n):          │
│                                     │             for j in range(n):      │
│ # Generic algorithm                 │                 if (dist[i][k] +    │
│ def apsp_semiring(W, n, semiring):  │                     dist[k][j] <    │
│     L = copy.deepcopy(W)            │                     dist[i][j]):    │
│     for _ in range(n-1):            │                     dist[i][j] = (  │
│         L = extend(L, W, semiring)  │                         dist[i][k] +│
│     return L                        │                         dist[k][j]) │
│                                     │     return dist                     │
│ # Works for ANY semiring!           │                                     │
├─────────────────────────────────────┼─────────────────────────────────────┤
│ ✓ Unified framework                 │ ✓ Direct, optimized                 │
│ ✓ Reusable for other problems       │ ✓ Easy to understand                │
│ ✓ Mathematical elegance             │ ✓ Well-known algorithm              │
│ ✗ Abstraction overhead              │ ✗ Problem-specific only             │
└─────────────────────────────────────┴─────────────────────────────────────┘
""")

    print(f"""
🎯 PROBLEM: Single-Source Shortest Path (SSSP)

┌─────────────────────────────────────┬─────────────────────────────────────┐
│ GENERALIZED (Same as above!)        │ TRADITIONAL (New implementation)    │
├─────────────────────────────────────┼─────────────────────────────────────┤
│                                     │                                     │
│ # Same semiring as APSP             │ def dijkstra(matrix, source):       │
│ # Same algorithm with source param  │     n = len(matrix)                 │
│                                     │     distances = [inf] * n           │
│ def sssp_semiring(W, n, semiring,   │     distances[source] = 0           │
│                   source):          │     visited = [False] * n           │
│     d = [semiring.zero] * n         │                                     │
│     d[source] = semiring.one        │     for _ in range(n):              │
│                                     │         min_dist = inf              │
│     for _ in range(n-1):            │         min_vertex = -1             │
│         d = extend_sssp(d, W,       │         for v in range(n):          │
│                        semiring)    │             if (not visited[v] and  │
│     return d                        │                 distances[v] <      │
│                                     │                 min_dist):          │
│ # Code reuse = 90%                  │                 min_dist = dist[v]  │
│                                     │                 min_vertex = v      │
│                                     │         # ... update neighbors ...  │
│                                     │     return distances                │
│                                     │                                     │
│                                     │ # Completely different algorithm!   │
├─────────────────────────────────────┼─────────────────────────────────────┤
│ ✓ Code reuse across problems        │ ✓ Optimal for sparse graphs         │
│ ✓ Consistent interface              │ ✓ Industry standard                 │
│ ✗ May not exploit graph structure   │ ✗ No code sharing with APSP        │
└─────────────────────────────────────┴─────────────────────────────────────┘
""")

    print(f"""
🎯 ADDING A NEW PROBLEM: Widest Path

┌─────────────────────────────────────┬─────────────────────────────────────┐
│ GENERALIZED (Just change semiring)  │ TRADITIONAL (New algorithm needed)  │
├─────────────────────────────────────┼─────────────────────────────────────┤
│                                     │                                     │
│ # New semiring definition           │ def widest_path_floyd(matrix):      │
│ widest_semiring = Semiring(         │     n = len(matrix)                 │
│     add=max,        # bottleneck    │     capacity = copy.copy(matrix)    │
│     multiply=min,   # path capacity │                                     │
│     zero=0,                         │     for k in range(n):              │
│     one=float('inf')                │         for i in range(n):          │
│ )                                   │             for j in range(n):      │
│                                     │                 capacity[i][j] = max(│
│ # SAME algorithm code!              │                     capacity[i][j], │
│ result = apsp_semiring(W, n,        │                     min(capacity[i][k],│
│                       widest_sem.)  │                         capacity[k][j])│
│                                     │                 )                   │
│ # 0 lines of new algorithm code     │     return capacity                 │
│                                     │                                     │
│                                     │ # ~15 lines of new algorithm code   │
├─────────────────────────────────────┼─────────────────────────────────────┤
│ ✓ Instant support for new problems  │ ✓ Can optimize for problem specifics│
│ ✓ Guaranteed correctness            │ ✗ Must implement & test each time  │
│ ✓ Minimal code maintenance          │ ✗ Code duplication and maintenance │
└─────────────────────────────────────┴─────────────────────────────────────┘
""")

def demonstrate_extensibility():
    """Show how easy it is to extend the generalized approach."""
    from testing_implementations import apsp_sssp, Semiring, generate_random_mtx_file, load_mtx_as_dense_list
    
    print("\n🚀 EXTENSIBILITY DEMONSTRATION")
    print("="*60)
    
    # Generate test matrix
    generate_random_mtx_file("extension_demo.mtx", n=4, density=0.7, symmetric=True)
    W = load_mtx_as_dense_list("extension_demo.mtx")
    n = len(W)
    
    print(f"Test matrix:")
    for i, row in enumerate(W):
        formatted = [f"{x:.0f}" if x != float('inf') else "∞" for x in row]
        print(f"  {formatted}")
    
    # Define multiple semirings
    problems = {
        "Shortest Path": Semiring(min, lambda x,y: x+y, float('inf'), 0),
        "Longest Path": Semiring(max, lambda x,y: x+y, float('-inf'), 0),
        "Widest Path": Semiring(max, min, 0, float('inf')),
        "Path Exists": Semiring(lambda x,y: x or y, lambda x,y: x and y, False, True),
        "Path Count": Semiring(lambda x,y: x+y, lambda x,y: x*y, 0, 1)
    }
    
    print(f"\n📊 Results for different problems (same algorithm!):")
    
    for problem_name, semiring in problems.items():
        try:
            if "Path Exists" in problem_name:
                # Convert to boolean matrix
                W_bool = [[bool(W[i][j]) if W[i][j] != float('inf') else False for j in range(n)] for i in range(n)]
                result = apsp_sssp(W_bool, n, semiring)
            elif "Path Count" in problem_name:
                # For path counting, use 1 for edges, 0 for no edges
                W_count = [[1 if W[i][j] == 1.0 else 0 if W[i][j] == float('inf') else int(W[i][j]) for j in range(n)] for i in range(n)]
                result = apsp_sssp(W_count, n, semiring)
            elif "Longest Path" in problem_name:
                # For longest path, negate weights (works for DAGs)
                continue  # Skip this one as it's complex for general graphs
            else:
                # For other problems, modify weights appropriately
                if "Widest" in problem_name:
                    W_modified = [[1.0 if W[i][j] == 1.0 else 0.0 if W[i][j] == float('inf') else W[i][j] for j in range(n)] for i in range(n)]
                    result = apsp_sssp(W_modified, n, semiring)
                else:
                    result = apsp_sssp(W, n, semiring)
            
            print(f"\n{problem_name}:")
            for i in range(min(3, len(result))):
                if "Path Exists" in problem_name:
                    formatted = [str(result[i][j]) for j in range(min(4, len(result[i])))]
                elif "Path Count" in problem_name:
                    formatted = [str(result[i][j]) for j in range(min(4, len(result[i])))]
                else:
                    formatted = [f"{result[i][j]:.1f}" if result[i][j] not in [float('inf'), float('-inf')] else "∞" for j in range(min(4, len(result[i])))]
                print(f"  Row {i}: {formatted}")
                
        except Exception as e:
            print(f"\n{problem_name}: Skipped ({e})")
    
    print(f"\n💡 Key insight: ONE algorithm implementation solves MULTIPLE problems!")
    print(f"   Traditional approach would require separate algorithms for each.")

def print_maintenance_comparison():
    """Compare maintenance requirements."""
    
    print(f"\n🔧 MAINTENANCE & DEVELOPMENT COMPARISON")
    print("="*60)
    
    comparison = f"""
📊 Development Metrics:

┌─────────────────────┬──────────────┬──────────────┐
│ Metric              │ Generalized  │ Traditional  │
├─────────────────────┼──────────────┼──────────────┤
│ Core Algorithm Code │ ~50 lines    │ ~30 per alg. │
│ Lines per Problem   │ ~5 lines     │ ~30-50 lines │
│ Code Reuse          │ 90%+         │ 10-20%       │
│ Testing Complexity  │ Test once    │ Test each    │
│ Bug Fix Impact      │ All problems │ One problem  │
│ New Developer Time  │ Learn once   │ Learn each   │
│ Extension Effort    │ Minutes      │ Days/Weeks   │
└─────────────────────┴──────────────┴──────────────┘

🎯 When to Choose Which:

GENERALIZED (Semiring-based):
✅ Research environments
✅ Educational settings  
✅ Rapid prototyping
✅ Multiple similar problems
✅ Mathematical correctness critical
✅ Long-term maintainability

TRADITIONAL (Problem-specific):
✅ Production systems
✅ Performance-critical applications
✅ Well-understood single problems
✅ Large sparse graphs
✅ Memory-constrained environments
✅ Team familiar with classical algorithms

🔮 Future Considerations:
• Generalized approaches are better for AI/ML integration
• Traditional approaches have more optimization research
• Hybrid approaches can combine benefits of both
"""
    
    print(comparison)

def main():
    """Run the code comparison demonstration."""
    print("📋 GENERALIZED vs TRADITIONAL: CODE COMPARISON")
    print("="*80)
    
    # 1. Show code structure differences
    print_code_comparison()
    
    # 2. Demonstrate extensibility
    demonstrate_extensibility()
    
    # 3. Compare maintenance aspects
    print_maintenance_comparison()
    
    print(f"\n🎉 CONCLUSION:")
    print(f"Both approaches have their place in computer science!")
    print(f"• Generalized: Elegance, flexibility, mathematical beauty")
    print(f"• Traditional: Performance, familiarity, optimization")
    print(f"• Best choice depends on your specific needs and constraints")

if __name__ == "__main__":
    main()
