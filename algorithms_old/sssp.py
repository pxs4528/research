from typing import List, Callable, TypeVar
from core.semiring import Semiring

T = TypeVar("T")


def single_source_shortest_path(
    W: List[List[T]], source: int, n: int, semiring: Semiring
) -> List[T]:

    d = [semiring.zero] * n
    d[source] = semiring.one

    for _ in range(n - 1):
        d_new = [semiring.zero] * n
        for i in range(n):
            for j in range(n):
                d_new[i] = semiring.add(
                    d_new[i], semiring.multiply(W[i][j], d[j]))
        d = d_new

    return d
