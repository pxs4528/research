"""
Generalized graph algorithms using semiring structures.

This module implements generalized versions of common graph algorithms
that work with any semiring structure.
"""

from typing import List, TypeVar
from src.core.semiring import Semiring

T = TypeVar("T")


def extended(L_prev: List[T], W: List[List[T]], n: int, semiring: Semiring, source: int = None) -> List[T]:
    """
    Extended operation for APSP/SSSP algorithms.
    
    Args:
        L_prev: Previous iteration matrix/vector
        W: Weight matrix
        n: Matrix size
        semiring: Semiring structure to use
        source: Source vertex for SSSP (None for APSP)
        
    Returns:
        Updated matrix/vector
    """
    if source is None:
        # All-pairs case
        L_new = [[semiring.zero for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    L_new[i][j] = semiring.add(L_new[i][j], semiring.multiply(L_prev[i][k], W[k][j]))
        return L_new
    else:
        # Single-source case
        d_new = [semiring.zero] * n
        for i in range(n):
            for j in range(n):
                d_new[i] = semiring.add(d_new[i], semiring.multiply(W[i][j], L_prev[j]))
        return d_new


def apsp_sssp(W: List[List[T]], n: int, semiring: Semiring, source: int = None) -> List[List[T]]:
    """
    Unified APSP/SSSP algorithm using semiring operations.
    
    Args:
        W: Weight matrix
        n: Matrix size
        semiring: Semiring structure to use
        source: Source vertex for SSSP (None for APSP)
        
    Returns:
        Distance matrix (APSP) or distance vector wrapped in list (SSSP)
    """
    if source is not None:
        # Single-source shortest path
        d = [semiring.zero] * n
        d[source] = semiring.one

        for _ in range(n - 1):
            d = extended(d, W, n, semiring, source=source)
        return [d]  # Return as list of lists for consistency
    else:
        # All-pairs shortest path
        L = [row[:] for row in W]
        for _ in range(n - 1):
            L = extended(L, W, n, semiring)
        return L


def extend_shortest_paths(L_prev: List[List[T]], W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    """
    Single iteration of shortest path extension.
    
    Args:
        L_prev: Previous distance matrix
        W: Weight matrix
        n: Matrix size
        semiring: Semiring structure to use
        
    Returns:
        Updated distance matrix
    """
    L_new = [[semiring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                L_new[i][j] = semiring.add(L_new[i][j], semiring.multiply(L_prev[i][k], W[k][j]))
    return L_new


def slow_apsp(W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    """
    Slow all-pairs shortest path algorithm using repeated matrix powers.
    
    Args:
        W: Weight matrix
        n: Matrix size
        semiring: Semiring structure to use
        
    Returns:
        Distance matrix
    """
    L = [row[:] for row in W]
    for r in range(1, n):
        L = extend_shortest_paths(L, W, n, semiring)
    return L


def generalized_mst(W: List[List[T]], n: int, semiring: Semiring) -> List[tuple]:
    """
    Generalized Minimum Spanning Tree using semiring operations.
    
    This implements a Prim's-like algorithm generalized to work with any semiring.
    For MST, we use the shortest path semiring (min, +, inf, 0).
    
    Args:
        W: Weight matrix (adjacency matrix with edge weights)
        n: Number of vertices
        semiring: Semiring structure (use SHORTEST_PATH_SEMIRING for MST)
        
    Returns:
        List of edges (u, v, weight) in the MST
    """
    if n == 0:
        return []
    
    # Track vertices in MST
    in_mst = [False] * n
    # Minimum edge weight to reach each vertex
    min_edge = [semiring.zero] * n
    # Parent of each vertex in MST
    parent = [-1] * n
    # MST edges
    mst_edges = []
    
    # Start from vertex 0
    min_edge[0] = semiring.one
    
    for _ in range(n):
        # Find vertex with minimum edge weight
        u = -1
        for v in range(n):
            if not in_mst[v]:
                if u == -1 or semiring.add(min_edge[v], min_edge[u]) == min_edge[v]:
                    u = v
        
        # Add vertex to MST
        in_mst[u] = True
        
        # Add edge to result (except for first vertex)
        if parent[u] != -1:
            mst_edges.append((parent[u], u, W[parent[u]][u]))
        
        # Update minimum edges to adjacent vertices
        for v in range(n):
            if not in_mst[v] and W[u][v] != semiring.zero:
                # Check if edge (u,v) gives better connection to v
                if (min_edge[v] == semiring.zero or 
                    semiring.add(W[u][v], min_edge[v]) == W[u][v]):
                    min_edge[v] = W[u][v]
                    parent[v] = u
    
    return mst_edges
