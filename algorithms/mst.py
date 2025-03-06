from typing import List, Callable, TypeVar
from core.semiring import Semiring

T = TypeVar("T")


def mst_matrix_multiplication(W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    mst_edges = []
    visited = [False] * n
    visited[0] = True

    while len(mst_edges) < n - 1:
        min_edge = (None, None, semiring.zero)

        for u in range(n):
            if visited[u]:
                for v in range(n):
                    if not visited[v] and W[u][v] != semiring.zero:
                        if semiring.add(min_edge[2], W[u][v]) == W[u][v]:
                            min_edge = (u, v, W[u][v])

        u, v, weight = min_edge
        mst_edges.append((u, v, weight))
        visited[v] = True

    return mst_edges

