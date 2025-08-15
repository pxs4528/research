from typing import List
from algorithms.apsp import slow_apsp
from algorithms.apsp_sssp import apsp_sssp
from core.semiring import Semiring
from scipy.io import mmread
import numpy as np
import os

def load_mtx_as_dense_list(path: str, inf=float("inf")) -> List[List[float]]:
    try:
        print(f"Loading matrix from {path}...")
        sparse_matrix = mmread(path)
        print("Matrix loaded successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to read .mtx file: {e}")

    n = max(sparse_matrix.shape)
    dense = [[inf] * n for _ in range(n)]

    for i, j in zip(sparse_matrix.row, sparse_matrix.col):
        dense[i][j] = 1
        dense[j][i] = 1  # if symmetric

    for i in range(n):
        dense[i][i] = 0
    print("Loaded matrix with size:", n, "x", n)
    return dense

if __name__ == "__main__":
    inf = float('inf')
    shortest_path_semiring = Semiring(
        add=min,
        multiply=lambda x, y: x + y,
        zero=inf,
        one=0
    )
    print("Using Semiring for Shortest Path:")

    # W = [
    #     [0, 3, inf, inf],
    #     [inf, 0, 1, inf],
    #     [inf, inf, 0, 7],
    #     [2, inf, inf, 0]
    # ]

    W = load_mtx_as_dense_list("A2.mtx", inf=inf)
    print("Input Matrix W:")
    for row in W:
        print(row)
    if not W:
        raise ValueError("The input matrix W is empty or not loaded correctly.")

    n = len(W)
    shortest_paths = apsp_sssp(W, n, shortest_path_semiring)

    print("All-Pairs Shortest Path Matrix from generlised with A2:")
    for row in shortest_paths:
        print(row)

    shortest_path = slow_apsp(W, n, shortest_path_semiring)

    print("\nAll-Pairs Shortest Path Matrix from Normal:")
    for row in shortest_path:
        print(row)
