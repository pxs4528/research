import unittest
from algorithms_old.apsp import slow_apsp
from core.semiring import Semiring

class TestAPSP(unittest.TestCase):
    def test_apsp(self):
        inf = float('inf')
        shortest_path_semiring = Semiring(
            add=min,
            multiply=lambda x, y: x + y,
            zero=inf,
            one=0
        )

        W = [
            [0, 3, inf],
            [inf, 0, 1],
            [inf, inf, 0]
        ]

        expected_result = [
            [0, 3, 4],
            [inf, 0, 1],
            [inf, inf, 0]
        ]

        result = slow_apsp(W, len(W), shortest_path_semiring)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
