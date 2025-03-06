from typing import List, Callable, TypeVar

T = TypeVar("T")

class Semiring:
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one

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
    
    shortest_paths = slow_apsp(W, n, shortest_path_semiring)
    
    print("All-Pairs Shortest Path Matrix:")
    for row in shortest_paths:
        print(row)
