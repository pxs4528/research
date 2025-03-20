from typing import List, Tuple, TypeVar, Callable

T = TypeVar("T")

class Semiring:
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one

def min_plus_product(A: List[List[T]], B: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    """Matrix multiplication in the min-plus semiring."""
    C = [[semiring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if A[i][k] != semiring.zero and B[k][j] != semiring.zero:
                    C[i][j] = min(C[i][j], semiring.multiply(A[i][k], B[k][j]))
    return C

def mst_matrix_boruvka(W: List[List[T]], n: int, semiring: Semiring) -> List[Tuple[int, int, T]]:
    """Borůvka’s MST algorithm using matrix operations."""
    MST = []
    components = list(range(n))  
    L = [row[:] for row in W]  # Copy of the weight matrix

    while len(set(components)) > 1:
        L = min_plus_product(L, W, n, semiring)  # Compute next power of adjacency matrix

        min_edges = [None] * n  
        for u in range(n):
            for v in range(n):
                if components[u] != components[v] and L[u][v] != semiring.zero and L[u][v] != semiring.zero:
                    # Ensure we're selecting a **valid edge** (i.e., not `inf`)
                    if min_edges[components[u]] is None or L[u][v] < min_edges[components[u]][2]:
                        min_edges[components[u]] = (u, v, W[u][v])  # Use W instead of L

        merged = set()
        for edge in min_edges:
            if edge:
                u, v, weight = edge
                if weight == semiring.zero:  # Skip invalid edges
                    continue
                if components[u] in merged or components[v] in merged:
                    continue  # Prevent multiple merges per iteration

                MST.append((u, v, weight))
                merged.add(components[u])
                merged.add(components[v])

                # Merge components
                old_comp, new_comp = components[v], components[u]
                for i in range(n):
                    if components[i] == old_comp:
                        components[i] = new_comp

    return MST

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
        [inf, 3, inf, 7],
        [6, 8, 7, inf]
    ]

    n = len(W)
    mst_edges = mst_matrix_boruvka(W, n, mst_semiring)

    print("Edges in the Minimum Spanning Tree:")
    for u, v, weight in sorted(mst_edges):
        print(f"({u}, {v}) with weight {weight}")
