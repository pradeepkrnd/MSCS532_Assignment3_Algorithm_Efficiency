"""Basic correctness tests for Assignment 3."""

import unittest

from hash_table_chaining import HashTableChaining
from quicksort_analysis import deterministic_quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    def test_edge_cases(self) -> None:
        cases = [[], [1], [2, 1], [3, 3, 1, 2, 3], list(range(20)), list(range(20, 0, -1))]
        for case in cases:
            expected = sorted(case)
            self.assertEqual(randomized_quicksort(case, seed=42), expected)
            self.assertEqual(deterministic_quicksort(case), expected)


class HashTableTests(unittest.TestCase):
    def test_insert_search_update_delete(self) -> None:
        table = HashTableChaining[str](capacity=3)
        table.insert(1, "one")
        table.insert(4, "four")
        table.insert(7, "seven")
        self.assertEqual(table.search(4), "four")
        table.insert(4, "FOUR")
        self.assertEqual(table.search(4), "FOUR")
        self.assertTrue(table.delete(1))
        self.assertIsNone(table.search(1))
        self.assertFalse(table.delete(999))

    def test_resize_preserves_values(self) -> None:
        table = HashTableChaining[int](capacity=3, max_load_factor=0.60)
        for key in range(100):
            table.insert(key, key * key)
        for key in range(100):
            self.assertEqual(table.search(key), key * key)
        self.assertLessEqual(table.load_factor, 0.60)


if __name__ == "__main__":
    unittest.main()
