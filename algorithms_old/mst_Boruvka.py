from typing import List, TypeVar
from core.semiring import Semiring

T = TypeVar("T")

def extend_mst(L_prev: List[List[T]], W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    L_new = [[semiring.zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                L_new[i][j] = min(L_new[i][j], (L_prev[i][k] + W[k][j]))
    return L_new

def slow_mst(W: List[List[T]], n: int, semiring: Semiring) -> List[List[T]]:
    L = [row[:] for row in W]
    for r in range(1, n):
        L = extend_mst(L, W, n, semiring)
    return L

# W = [
#     [0, 1, 4, float('inf')],
#     [1, 0, 2, 3],
#     [4, 2, 0, 3],
#     [float('inf'), 3, 3, 0]
# ]

W = [
    [0, 2, 4, float('inf'), 3],
    [2, 0, 3, 5, float('inf')],
    [4, 3, 0, 5, 4],
    [float('inf'), 5, 5, 0, 2],
    [3, float('inf'), 4, 2, 0]
]


n = len(W)

semiring = Semiring(
    add=min,
    multiply=lambda x, y: x + y,
    zero=float('inf'),
    one=0
)

mst = slow_mst(W, n, semiring)

for row in mst:
    print(row)
