"""
Backward compatibility module for Boggle Engine.
Redirects to the modular architecture in src.boggle.models.
"""
from src.boggle.models.trie import Trie, TrieNode
from src.boggle.models.board import Board
from src.boggle.models.solver import BoggleSolver
from src.boggle.models.scoring import get_word_score, calculate_rank

# Alias for old engine class name
BoggleEngine = BoggleSolver

__all__ = [
    "Trie",
    "TrieNode",
    "Board",
    "BoggleSolver",
    "BoggleEngine",
    "get_word_score",
    "calculate_rank",
]
