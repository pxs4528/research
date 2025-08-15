"""
Matrix utilities for loading and manipulating graph matrices.

This module provides utilities for loading Matrix Market files and
converting between different matrix formats.
"""

import os
from typing import List
import numpy as np
from scipy import sparse
from scipy.io import mmread, mmwrite


def generate_random_mtx_file(
    filename: str,
    n: int,
    density: float = 0.1,
    symmetric: bool = False,
    pattern: bool = True,
    dtype=np.float64,
) -> None:
    """Generate a random Matrix Market file for testing."""
    A = sparse.random(n, n, density=density, format='coo', dtype=dtype)

    if symmetric:
        A = A + A.T

    if pattern:
        A.data[:] = 1  # Pattern matrix (boolean entries only)

    mmwrite(filename, A)
    print(f"Generated random matrix: {filename}")


def load_mtx_as_dense_list(path: str, inf_value: float = float("inf")) -> List[List[float]]:
    """Load a Matrix Market file and convert to dense adjacency list format."""
    try:
        print(f"Loading matrix from {path}...")
        
        # Try to read with scipy first
        try:
            sparse_matrix = mmread(path)
            print(f"Matrix loaded successfully: {sparse_matrix.shape}")
            print(f"Matrix format: {sparse_matrix.format}")
            print(f"Matrix data type: {sparse_matrix.dtype}")
        except Exception as scipy_error:
            print(f"Scipy failed: {scipy_error}")
            print("Attempting manual parsing...")
            
            # Manual parsing for problematic format
            with open(path, 'r') as f:
                lines = f.readlines()
            
            # Skip comments
            data_lines = []
            for line in lines:
                if not line.startswith('%'):
                    data_lines.append(line.strip())
            
            # Parse header
            header = data_lines[0].split()
            n_rows, n_cols = int(header[0]), int(header[1])
            n = max(n_rows, n_cols)
            
            # Create the matrix manually
            dense = [[inf_value] * n for _ in range(n)]
            
            # Parse edges
            for line in data_lines[1:]:
                if line:
                    parts = line.split()
                    i, j = int(parts[0]) - 1, int(parts[1]) - 1  # Convert to 0-based indexing
                    if i < n and j < n:
                        dense[i][j] = 1.0
                        dense[j][i] = 1.0  # Symmetric
            
            # Set diagonal to 0
            for i in range(n):
                dense[i][i] = 0.0
                
            print(f"Manually parsed matrix: {n}x{n}")
            return dense
                
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise RuntimeError(f"Failed to read .mtx file: {e}")

    n = max(sparse_matrix.shape)
    dense = [[inf_value] * n for _ in range(n)]

    # Convert to COO format if needed
    if hasattr(sparse_matrix, 'tocoo'):
        sparse_matrix = sparse_matrix.tocoo()
    else:
        print(f"Warning: Matrix doesn't have tocoo method. Type: {type(sparse_matrix)}")

    # Fill in the edges
    try:
        for i, j in zip(sparse_matrix.row, sparse_matrix.col):
            if i < n and j < n:  # Safety check
                dense[i][j] = 1.0
                if i != j:  # For symmetric graphs, add reverse edge unless it's a self-loop
                    dense[j][i] = 1.0
    except AttributeError as e:
        print(f"Error accessing matrix data: {e}")
        print(f"Matrix type: {type(sparse_matrix)}")
        print(f"Matrix attributes: {dir(sparse_matrix)}")
        raise

    # Set diagonal to 0 (distance to self)
    for i in range(n):
        dense[i][i] = 0.0
        
    print(f"Converted to dense matrix: {n}x{n}")
    return dense


def find_mtx_files(directory: str = ".") -> List[str]:
    """Find all Matrix Market files in the specified directory."""
    pattern = os.path.join(directory, "*.mtx")
    import glob
    return glob.glob(pattern)
