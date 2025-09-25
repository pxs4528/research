# Graph Algorithms Research Project

A comprehensive framework for comparing generalized semiring-based graph algorithms with traditional implementations.

## Project Structure

```
research/
├── src/                          # Core source code
│   ├── core/                    # Core data structures
│   │   └── semiring.py          # Semiring definitions and common semirings
│   ├── algorithms/              # Algorithm implementations
│   │   ├── generalized.py       # Generalized semiring-based algorithms
│   │   └── traditional.py       # Traditional algorithm implementations
│   └── utils/                   # Utility modules
│       ├── matrix_utils.py      # Matrix loading and generation utilities
│       └── testing_framework.py # Algorithm testing framework
├── comparisons/                 # Comparison and analysis scripts
│   ├── basic_comparison.py      # Basic performance comparison
│   ├── detailed_comparison.py   # Comprehensive analysis
│   └── code_comparison.py       # Code structure comparison
├── test_data/                   # Matrix Market test files (.mtx)
├── test_results/               # Test output and results
├── examples/                   # Example usage scripts
├── tests/                      # Unit tests
└── main.py                     # Main entry point
```

## Quick Start

### Run Basic Tests

```bash
python main.py test
```

### Show Project Structure

```bash
python main.py structure
```

### Run Comparisons

```bash
# Basic comparison
python comparisons/basic_comparison.py
```

## Supported Algorithms

### Generalized Implementations

- All-Pairs Shortest Path (APSP)
- Single-Source Shortest Path (SSSP)
- Widest Path
- Path Reachability
- Path Counting

### Traditional Implementations

- Floyd-Warshall (APSP)
- Dijkstra (SSSP)
- Bellman-Ford (SSSP)
- Custom Widest Path

## Testing Framework

The `AlgorithmTester` class provides:

- Automated test file discovery
- Performance timing and comparison
- Result verification
- Flexible algorithm registration
- Formatted output display

## 🔧 Usage Examples

### Basic Testing

```python
from src import AlgorithmTester, SHORTEST_PATH_SEMIRING

tester = AlgorithmTester(SHORTEST_PATH_SEMIRING)
results = tester.run_tests("test_data/")
tester.display_results()
```

### Custom Algorithm Comparison

```python
from src import apsp_sssp, floyd_warshall, SHORTEST_PATH_SEMIRING
from src.utils.matrix_utils import load_mtx_as_dense_list

# Load test matrix
W = load_mtx_as_dense_list("test_data/graph.mtx")
n = len(W)

# Compare approaches
result_gen = apsp_sssp(W, n, SHORTEST_PATH_SEMIRING)
result_trad = floyd_warshall(W)
```

### Adding New Semirings

```python
from src.core.semiring import Semiring

# Define custom semiring
max_plus_semiring = Semiring(
    add=max,
    multiply=lambda x, y: x + y,
    zero=float('-inf'),
    one=0
)

# Use with generalized algorithms
result = apsp_sssp(W, n, max_plus_semiring)
```
