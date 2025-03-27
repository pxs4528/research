from typing import List, Tuple, TypeVar, Callable
from core.semiring import Semiring

T = TypeVar("T")

class Semiring:
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one

def min_plus_product(A: List[List[T]], B: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    C = [[semiring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # if A[i][k] != semiring.zero and B[k][j] != semiring.zero:
                C[i][j] = min(C[i][j], semiring.multiply(A[i][k], B[k][j]))
    return C

def mst_matrix_boruvka(W: List[List[T]], n: int, semiring: Semiring) -> List[Tuple[int, int, T]]:
    MST = []
    components = list(range(n))  
    L = [row[:] for row in W]

    while len(set(components)) > 1:
        L = min_plus_product(L, W, n, semiring)
        min_edges = [None] * n  
        for u in range(n):
            for v in range(n):
                if components[u] != components[v] and L[u][v] != semiring.zero and L[u][v] != semiring.zero:
                    if min_edges[components[u]] is None or L[u][v] < min_edges[components[u]][2]:
                        min_edges[components[u]] = (u, v, W[u][v])

        merged = set()
        for edge in min_edges:
            if edge:
                u, v, weight = edge
                if weight == semiring.zero:
                    continue
                if components[u] in merged or components[v] in merged:
                    continue

                MST.append((u, v, weight))
                merged.add(components[u])
                merged.add(components[v])

                old_comp, new_comp = components[v], components[u]
                for i in range(n):
                    if components[i] == old_comp:
                        components[i] = new_comp

    return MST