from typing import List, Callable, TypeVar

T = TypeVar("T")

class Semiring:
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one

def single_source_shortest_path(
    W: List[List[T]], source: int, n: int, semiring: Semiring
) -> List[T]:

    d = [semiring.zero] * n
    d[source] = semiring.one

    for _ in range(n - 1):
        d_new = [semiring.zero] * n
        for i in range(n):
            for j in range(n):
                d_new[i] = semiring.add(d_new[i], semiring.multiply(W[i][j], d[j]))
        d = d_new

    return d

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
