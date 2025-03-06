from algorithms.sssp import single_source_shortest_path
from core.semiring import Semiring

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

    distances = single_source_shortest_path(W, source_vertex, n, shortest_path_semiring)

    print(f"Shortest distances from vertex {source_vertex}:")
    print(distances)
