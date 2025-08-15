"""
Traditional graph algorithms implementations.

This module contains classic implementations of graph algorithms
for comparison with the generalized semiring-based approaches.
"""

from typing import List


def floyd_warshall(adj_matrix: List[List[float]]) -> List[List[float]]:
    """
    Traditional Floyd-Warshall algorithm for All-Pairs Shortest Path.
    
    Time Complexity: O(n^3)
    Space Complexity: O(n^2)
    
    Args:
        adj_matrix: Adjacency matrix representation of the graph
        
    Returns:
        Distance matrix with shortest paths between all pairs
    """
    n = len(adj_matrix)
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Copy the adjacency matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif adj_matrix[i][j] == 1:  # There's an edge
                dist[i][j] = 1
    
    # Floyd-Warshall main algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


def dijkstra(adj_matrix: List[List[float]], source: int) -> List[float]:
    """
    Traditional Dijkstra algorithm for Single-Source Shortest Path.
    
    Time Complexity: O(V^2) for dense graphs with simple implementation
    Space Complexity: O(V)
    
    Args:
        adj_matrix: Adjacency matrix representation of the graph
        source: Source vertex
        
    Returns:
        Distance vector from source to all vertices
    """
    n = len(adj_matrix)
    distances = [float('inf')] * n
    distances[source] = 0
    visited = [False] * n
    
    for _ in range(n):
        # Find minimum distance vertex
        min_dist = float('inf')
        min_vertex = -1
        for v in range(n):
            if not visited[v] and distances[v] < min_dist:
                min_dist = distances[v]
                min_vertex = v
        
        if min_vertex == -1:
            break
            
        visited[min_vertex] = True
        
        # Update distances to neighbors
        for neighbor in range(n):
            if (not visited[neighbor] and 
                adj_matrix[min_vertex][neighbor] == 1 and 
                distances[min_vertex] + 1 < distances[neighbor]):
                distances[neighbor] = distances[min_vertex] + 1
    
    return distances


def bellman_ford(adj_matrix: List[List[float]], source: int) -> List[float]:
    """
    Traditional Bellman-Ford algorithm for Single-Source Shortest Path.
    
    Time Complexity: O(VE) = O(V^3) for dense graphs
    Space Complexity: O(V)
    
    Args:
        adj_matrix: Adjacency matrix representation of the graph
        source: Source vertex
        
    Returns:
        Distance vector from source to all vertices
    """
    n = len(adj_matrix)
    distances = [float('inf')] * n
    distances[source] = 0
    
    # Relax edges repeatedly
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if adj_matrix[u][v] == 1 and distances[u] + 1 < distances[v]:
                    distances[v] = distances[u] + 1
    
    return distances


def widest_path_floyd(adj_matrix: List[List[float]]) -> List[List[float]]:
    """
    Traditional implementation of widest path algorithm using Floyd-Warshall approach.
    
    Args:
        adj_matrix: Adjacency matrix with edge capacities
        
    Returns:
        Matrix with maximum capacities between all pairs
    """
    n = len(adj_matrix)
    capacity = [[0.0] * n for _ in range(n)]
    
    # Initialize capacity matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                capacity[i][j] = float('inf')  # Infinite capacity to self
            elif adj_matrix[i][j] == 1:
                capacity[i][j] = 1.0  # Edge capacity
    
    # Main widest path algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                capacity[i][j] = max(
                    capacity[i][j],
                    min(capacity[i][k], capacity[k][j])
                )
    
    return capacity


def kruskal_mst(adj_matrix: List[List[float]]) -> List[tuple]:
    """
    Traditional Kruskal's algorithm for Minimum Spanning Tree.
    """
    n = len(adj_matrix)
    edges = []
    
    # Extract edges from adjacency matrix
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] != float('inf') and adj_matrix[i][j] > 0:
                edges.append((i, j, adj_matrix[i][j]))
    
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    # Union-Find for cycle detection
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            parent[root_x] = root_y
            return True
        return False
    
    mst_edges = []
    for u, v, weight in edges:
        if union(u, v):
            mst_edges.append((u, v, weight))
            if len(mst_edges) == n - 1:
                break
    
    return mst_edges


def prim_mst(adj_matrix: List[List[float]]) -> List[tuple]:
    """
    Traditional Prim's algorithm for Minimum Spanning Tree.
    """
    n = len(adj_matrix)
    if n == 0:
        return []
    
    visited = [False] * n
    min_edge = [float('inf')] * n
    parent = [-1] * n
    mst_edges = []
    
    # Start from vertex 0
    min_edge[0] = 0
    
    for _ in range(n):
        # Find minimum edge vertex
        u = -1
        for v in range(n):
            if not visited[v] and (u == -1 or min_edge[v] < min_edge[u]):
                u = v
        
        visited[u] = True
        
        # Add edge to MST
        if parent[u] != -1:
            mst_edges.append((parent[u], u, adj_matrix[parent[u]][u]))
        
        # Update adjacent vertices
        for v in range(n):
            if (not visited[v] and adj_matrix[u][v] != float('inf') and 
                adj_matrix[u][v] < min_edge[v]):
                min_edge[v] = adj_matrix[u][v]
                parent[v] = u
    
    return mst_edges
