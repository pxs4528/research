from typing import List, TypeVar
from core.semiring import Semiring

T = TypeVar("T")

def extend_shortest_paths(L_prev: List[List[T]], W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    L_new = [[semiring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                L_new[i][j] = semiring.add(L_new[i][j], semiring.multiply(L_prev[i][k], W[k][j]))
    return L_new

def slow_apsp(W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    L = [row[:] for row in W]
    for r in range(1, n):
        L = extend_shortest_paths(L, W, n, semiring)
    return L
