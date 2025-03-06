from typing import List, Callable, TypeVar

T = TypeVar("T")

class Semiring:
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one

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

if __name__ == "__main__":
    inf = float('inf')

    mst_semiring = Semiring(
        add=min, 
        multiply=lambda x, y: x + y if x != inf and y != inf else inf,
        zero=inf,
        one=0
    )

    W = [
        [inf, 2, inf, 6],
        [2, inf, 3, 8],
        [inf, 3, inf, inf],
        [6, 8, inf, inf]
    ]

    n = len(W)

    mst_edges = mst_matrix_multiplication(W, n, mst_semiring)

    print("Edges in the Minimum Spanning Tree:")
    for u, v, weight in mst_edges:
        print(f"({u}, {v}) with weight {weight}")
