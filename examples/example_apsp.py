from algorithms.apsp import slow_apsp
from algorithms.apsp_sssp import apsp_sssp
from core.semiring import Semiring

if __name__ == "__main__":
    inf = float('inf')
    shortest_path_semiring = Semiring(
        add=min,
        multiply=lambda x, y: x + y,
        zero=inf,
        one=0
    )

    W = [
        [0, 3, inf, inf],
        [inf, 0, 1, inf],
        [inf, inf, 0, 7],
        [2, inf, inf, 0]
    ]

    n = len(W)
    shortest_paths = apsp_sssp(W, n, shortest_path_semiring)

    print("All-Pairs Shortest Path Matrix from generlised:")
    for row in shortest_paths:
        print(row)

    shortest_path = slow_apsp(W, n, shortest_path_semiring)

    print("\nAll-Pairs Shortest Path Matrix from Normal:")
    for row in shortest_path:
        print(row)