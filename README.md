# Assignment 3: Understanding Algorithm Efficiency and Scalability

This repository contains Python implementations and analysis materials for:

1. Randomized Quicksort compared with deterministic first-pivot Quicksort.
2. A hash table using separate chaining, universal hashing, and dynamic resizing.

## Files

- `quicksort_analysis.py` - both Quicksort versions and empirical benchmarks.
- `hash_table_chaining.py` - hash table implementation.
- `test_algorithms.py` - correctness tests.

## Requirements
- Python 3.10 or later
- No third-party packages are required to run the code.

## Run the programs
```bash
python quicksort_analysis.py
python hash_table_chaining.py
python -m unittest test_algorithms.py -v

## Summary of findings
Random pivot selection protects Quicksort from consistently poor pivot choices on already sorted and reverse-sorted inputs.
Its expected running time is O(n log n), although this two-way partition implementation can still slow down when many keys are equal.
Deterministic first-pivot Quicksort can degrade to O(n^2) on ordered data.



