from algorithms_old.mst import mst_matrix_multiplication
from core.semiring import Semiring

if __name__ == "__main__":
    inf = float('inf')
    
    mst_semiring = Semiring(
        add=min,
        multiply=lambda x, y: x + y if x != inf and y != inf else inf,
        zero=inf,
        one=0
    )

    W = [
        [inf, 1, 4, inf],
        [1, inf, 2, 6],
        [4, 2, inf, 3],
        [inf, 6, 3, inf]
    ]

    n = len(W)
    
    mst_edges = mst_matrix_multiplication(W, n, mst_semiring)

    print("Edges in the Minimum Spanning Tree:")
    for u, v, weight in mst_edges:
        print(f"({u}, {v}) with weight {weight}")
