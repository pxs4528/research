"""
Semiring structures for algebraic graph operations.

This module defines the basic semiring structure and common semirings
used in graph algorithms.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


class Semiring:
    """Semiring structure for algebraic graph operations."""
    
    def __init__(self, add: Callable[[T, T], T], multiply: Callable[[T, T], T], zero: T, one: T):
        """
        Initialize a semiring.
        
        Args:
            add: Addition operation (⊕)
            multiply: Multiplication operation (⊗)
            zero: Additive identity (⊕-identity)
            one: Multiplicative identity (⊗-identity)
        """
        self.add = add
        self.multiply = multiply
        self.zero = zero
        self.one = one
    
    def __str__(self):
        return f"Semiring(zero={self.zero}, one={self.one})"


# Predefined semirings for common algorithms
SHORTEST_PATH_SEMIRING = Semiring(
    add=min,
    multiply=lambda x, y: x + y,
    zero=float('inf'),
    one=0
)

LONGEST_PATH_SEMIRING = Semiring(
    add=max,
    multiply=lambda x, y: x + y,
    zero=float('-inf'),
    one=0
)

WIDEST_PATH_SEMIRING = Semiring(
    add=max,
    multiply=min,
    zero=0,
    one=float('inf')
)

REACHABILITY_SEMIRING = Semiring(
    add=lambda x, y: x or y,
    multiply=lambda x, y: x and y,
    zero=False,
    one=True
)

PATH_COUNT_SEMIRING = Semiring(
    add=lambda x, y: x + y,
    multiply=lambda x, y: x * y,
    zero=0,
    one=1
)
