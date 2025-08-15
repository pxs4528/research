import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.algorithms.generalized import apsp_sssp
from src.core.semiring import Semiring

if __name__ == "__main__":
    inf = float('inf')

    shortest_path_semiring = Semiring(
        add=min,
        multiply=lambda x, y: x + y if x != inf and y != inf else inf,
        zero=inf,
        one=0
    )

    W = [
        [0, 3, inf, inf],
        [inf, 0, 1, inf],
        [inf, inf, 0, 7],
        [2, inf, inf, 0]
    ]

    source_vertex = 0

    n = len(W)

    # Using the generalized APSP/SSSP function with source parameter
    distances = apsp_sssp(W, n, shortest_path_semiring, source=source_vertex)

    print(f"Shortest distances from vertex {source_vertex}:")
    print(distances)

    distances = apsp_sssp(W, n, shortest_path_semiring, source=source_vertex)

    print(f"\nShortest distances from vertex {source_vertex} using generalized:")
    print(distances)