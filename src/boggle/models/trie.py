"""
Prefix Tree (Trie) data structure for ultra-fast word lookups and DFS pruning.
"""
from typing import Dict, Optional


class TrieNode:
    """Node in the Trie."""
    __slots__ = ('children', 'is_end_of_word', 'word')

    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.word: Optional[str] = None


class Trie:
    """Prefix Tree for O(L) insertion, exact lookup, and prefix branching."""

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word: str) -> None:
        """Insert a word into the Trie."""
        word = word.strip().lower()
        if not word:
            return
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end_of_word:
            node.is_end_of_word = True
            node.word = word
            self.word_count += 1

    def contains(self, word: str) -> bool:
        """Return True if the exact word is present in the Trie."""
        word = word.strip().lower()
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word starts with the given prefix."""
        prefix = prefix.strip().lower()
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    @classmethod
    def from_file(cls, filepath: str, min_length: int = 3) -> "Trie":
        """Load a text file into a Trie, filtering out words below min_length."""
        trie = cls()
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip().lower()
                if word.isalpha() and len(word) >= min_length:
                    trie.insert(word)
        return trie

