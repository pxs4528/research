from algorithms.mst_Boruvka import slow_mst
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
    mst_edges = slow_mst(W, n, mst_semiring)

    print(mst_edges)
    # print("Edges in the Minimum Spanning Tree:")
    # for u, v, weight in sorted(mst_edges):
    #     print(f"({u}, {v}) with weight {weight}")
