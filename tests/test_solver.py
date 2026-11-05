"""
Unit tests for Trie-pruned Boggle solver and path validator in both Freeform and Adjacent modes.
"""
import unittest
from src.boggle.models.board import Board
from src.boggle.models.trie import Trie
from src.boggle.models.solver import BoggleSolver


class TestSolver(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        for w in ["cat", "car", "cart", "art", "rat", "tar", "star", "rats"]:
            self.trie.insert(w)

        self.board = Board(size=3)
        # C A T
        # R X X
        # S X X
        self.board.set_custom("CATRXXSXX", 3)
        self.solver = BoggleSolver(board=self.board, trie=self.trie, rule_mode="FREEFORM")

    def test_freeform_any_order(self):
        """In Freeform mode, words can be formed from any tiles on the board, non-adjacent."""
        self.solver.set_rule_mode("FREEFORM")
        solutions = self.solver.solve()
        
        # 'cat', 'car', 'star', 'rats' should all be formed using available letters C, A, T, R, S
        self.assertIn("cat", solutions)
        self.assertIn("car", solutions)
        self.assertIn("star", solutions)
        self.assertIn("rats", solutions)

        # Path tiles should contain distinct coordinates on the board
        path = solutions["star"]
        self.assertEqual(len(path), 4)
        self.assertEqual(len(set(path)), 4)  # No tile reused

    def test_adjacent_mode(self):
        """In Adjacent mode, words must use adjacent tiles."""
        self.solver.set_rule_mode("ADJACENT")
        solutions = self.solver.solve()
        self.assertIn("cat", solutions)
        self.assertIn("car", solutions)

        # In "CATRXXSXX":
        # S is at (2,0), T is at (0,2), A is at (0,1), R is at (1,0)
        # S (2,0) is NOT adjacent to T (0,2) or A (0,1)
        # So "star" should NOT be formable in adjacent mode!
        self.assertNotIn("star", solutions)

    def test_word_validation_freeform(self):
        self.solver.set_rule_mode("FREEFORM")
        is_valid, msg, path = self.solver.validate("cat")
        self.assertTrue(is_valid)
        self.assertIsNotNone(path)

        # 'star' uses S, T, A, R which are all on the board
        is_valid, msg, path = self.solver.validate("star")
        self.assertTrue(is_valid)

        # Word not in dictionary
        is_valid, msg, path = self.solver.validate("cax")
        self.assertFalse(is_valid)

        # Word too short (< 3 letters)
        is_valid, msg, path = self.solver.validate("ca")
        self.assertFalse(is_valid)

        # Word requires letter not on board (e.g. 'z')
        self.trie.insert("czar")
        is_valid, msg, path = self.solver.validate("czar")
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
