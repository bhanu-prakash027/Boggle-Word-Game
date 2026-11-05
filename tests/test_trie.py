"""
Unit tests for the Trie data structure.
"""
import unittest
from src.boggle.models.trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.words = ["apple", "apply", "app", "application", "banana", "band", "cat"]
        for w in self.words:
            self.trie.insert(w)

    def test_word_count(self):
        self.assertEqual(self.trie.word_count, len(self.words))

    def test_exact_lookup(self):
        self.assertTrue(self.trie.contains("apple"))
        self.assertTrue(self.trie.contains("APPLE"))  # Case-insensitive
        self.assertTrue(self.trie.contains("cat"))
        self.assertFalse(self.trie.contains("dog"))
        self.assertFalse(self.trie.contains("ap"))

    def test_prefix_checking(self):
        self.assertTrue(self.trie.starts_with("app"))
        self.assertTrue(self.trie.starts_with("ban"))
        self.assertTrue(self.trie.starts_with("c"))
        self.assertFalse(self.trie.starts_with("xyz"))
        self.assertFalse(self.trie.starts_with("cot"))


if __name__ == "__main__":
    unittest.main()

