"""Randomized and deterministic Quicksort implementations and benchmark utilities."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, Iterable, List, Sequence


def _partition_lomuto(values: List[int], low: int, high: int) -> int:
    """Partition values[low:high+1] using the element at high as pivot."""
    pivot = values[high]
    boundary = low - 1
    for index in range(low, high):
        if values[index] <= pivot:
            boundary += 1
            values[boundary], values[index] = values[index], values[boundary]
    values[boundary + 1], values[high] = values[high], values[boundary + 1]
    return boundary + 1


def randomized_quicksort(values: Sequence[int], seed: int | None = None) -> List[int]:
    """Return a sorted copy using uniformly random pivots and an explicit stack."""
    result = list(values)
    if len(result) < 2:
        return result

    rng = random.Random(seed)
    stack: list[tuple[int, int]] = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        pivot_index = rng.randint(low, high)
        result[pivot_index], result[high] = result[high], result[pivot_index]
        pivot_final = _partition_lomuto(result, low, high)

        # Push the larger partition first so the smaller one is processed next.
        left = (low, pivot_final - 1)
        right = (pivot_final + 1, high)
        if (left[1] - left[0]) > (right[1] - right[0]):
            stack.append(left)
            stack.append(right)
        else:
            stack.append(right)
            stack.append(left)
    return result


def deterministic_quicksort(values: Sequence[int]) -> List[int]:
    """Return a sorted copy using the first element of each subarray as pivot."""
    result = list(values)
    if len(result) < 2:
        return result

    stack: list[tuple[int, int]] = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        # Move the first element to the Lomuto pivot position.
        result[low], result[high] = result[high], result[low]
        pivot_final = _partition_lomuto(result, low, high)
        stack.append((low, pivot_final - 1))
        stack.append((pivot_final + 1, high))
    return result


@dataclass(frozen=True)
class BenchmarkRow:
    distribution: str
    size: int
    randomized_ms: float
    deterministic_ms: float


def _measure(function: Callable[[Sequence[int]], List[int]], data: Sequence[int], repeats: int) -> float:
    timings: list[float] = []
    expected = sorted(data)
    for _ in range(repeats):
        start = time.perf_counter()
        output = function(data)
        elapsed = (time.perf_counter() - start) * 1000
        if output != expected:
            raise AssertionError(f"{function.__name__} returned an incorrect result")
        timings.append(elapsed)
    return sum(timings) / len(timings)


def generate_data(distribution: str, size: int, seed: int = 2026) -> list[int]:
    rng = random.Random(seed + size)
    if distribution == "Random":
        return [rng.randint(0, size * 10) for _ in range(size)]
    if distribution == "Sorted":
        return list(range(size))
    if distribution == "Reverse-sorted":
        return list(range(size, 0, -1))
    if distribution == "Repeated elements":
        return [rng.randint(0, 9) for _ in range(size)]
    raise ValueError(f"Unknown distribution: {distribution}")


def run_benchmarks(sizes: Iterable[int] = (250, 500, 1000, 2000), repeats: int = 3) -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []
    for distribution in ("Random", "Sorted", "Reverse-sorted", "Repeated elements"):
        for size in sizes:
            data = generate_data(distribution, size)
            randomized = _measure(lambda items: randomized_quicksort(items, seed=42), data, repeats)
            deterministic = _measure(deterministic_quicksort, data, repeats)
            rows.append(BenchmarkRow(distribution, size, randomized, deterministic))
    return rows


if __name__ == "__main__":
    samples = [[], [1], [3, 1, 2], [5, 5, 2, 5, 1], list(range(10))]
    for sample in samples:
        print(f"Input: {sample}")
        print(f"Randomized:    {randomized_quicksort(sample, seed=42)}")
        print(f"Deterministic: {deterministic_quicksort(sample)}")

    print("\nAverage benchmark time (milliseconds)")
    print("Distribution,Size,Randomized,Deterministic")
    for row in run_benchmarks():
        print(f"{row.distribution},{row.size},{row.randomized_ms:.3f},{row.deterministic_ms:.3f}")
