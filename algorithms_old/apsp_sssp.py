from typing import List, TypeVar
from core.semiring import Semiring

T = TypeVar("T")

def extended(L_prev: List[T], W: List[List[T]], n: int, semiring: Semiring, source: int = None) -> List[T]:
    if source is None:
        L_new = [[semiring.zero for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    L_new[i][j] = semiring.add(L_new[i][j], semiring.multiply(L_prev[i][k], W[k][j]))
        return L_new
    else:
        d_new = [semiring.zero] * n
        for i in range(n):
            for j in range(n):
                d_new[i] = semiring.add(d_new[i], semiring.multiply(W[i][j], L_prev[j]))
        return d_new

def apsp_sssp(W: List[List[T]], n: int, semiring: Semiring, *args, **kwargs) -> List[List[T]]:
    source = kwargs.get("source", None)

    if source is not None:
        d = [semiring.zero] * n
        d[source] = semiring.one

        for _ in range(n - 1):
            d = extended(d, W, n, semiring, source=source)
        return d

    else:
        L = [row[:] for row in W]
        for _ in range(n - 1):
            L = extended(L, W, n, semiring)
        return L