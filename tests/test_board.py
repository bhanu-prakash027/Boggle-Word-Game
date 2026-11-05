"""
Unit tests for Board generation and dice rolling.
"""
import unittest
from src.boggle.models.board import Board


class TestBoard(unittest.TestCase):
    def test_board_sizes(self):
        board3 = Board(size=3)
        self.assertEqual(len(board3.grid), 3)
        self.assertEqual(len(board3.grid[0]), 3)

        board4 = Board(size=4)
        self.assertEqual(len(board4.grid), 4)
        self.assertEqual(len(board4.grid[0]), 4)

        board5 = Board(size=5)
        self.assertEqual(len(board5.grid), 5)
        self.assertEqual(len(board5.grid[0]), 5)

    def test_vowel_balancing(self):
        # Generate multiple boards and verify vowel presence
        vowels = set("AEIOU")
        for _ in range(10):
            board = Board(size=4)
            letters = [c for row in board.grid for c in row]
            v_count = sum(1 for c in letters if c in vowels)
            self.assertGreaterEqual(v_count, 3)

    def test_custom_board(self):
        board = Board(size=3)
        success = board.set_custom("ABCDEFGHI", 3)
        self.assertTrue(success)
        self.assertEqual(board.grid[0], ["A", "B", "C"])
        self.assertEqual(board.grid[1], ["D", "E", "F"])
        self.assertEqual(board.grid[2], ["G", "H", "I"])

        # Invalid length should fail
        fail = board.set_custom("TOOLONG12345", 3)
        self.assertFalse(fail)


if __name__ == "__main__":
    unittest.main()

