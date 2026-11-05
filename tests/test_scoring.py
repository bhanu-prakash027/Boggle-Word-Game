"""
Unit tests for Boggle scoring rules and rankings.
"""
import unittest
from src.boggle.models.scoring import get_word_score, calculate_rank


class TestScoring(unittest.TestCase):
    def test_scores_by_length(self):
        self.assertEqual(get_word_score("to"), 0)       # < 3 letters: 0 pts
        self.assertEqual(get_word_score("cat"), 1)      # 3 letters: 1 pt
        self.assertEqual(get_word_score("dogs"), 1)     # 4 letters: 1 pt
        self.assertEqual(get_word_score("apple"), 2)    # 5 letters: 2 pts
        self.assertEqual(get_word_score("banana"), 3)   # 6 letters: 3 pts
        self.assertEqual(get_word_score("morning"), 5)  # 7 letters: 5 pts
        self.assertEqual(get_word_score("wonderful"), 11) # 8+ letters: 11 pts

    def test_rank_calculation(self):
        rank, desc = calculate_rank(player_score=70, words_found=40, total_possible=60)
        self.assertIn("Grandmaster", rank)

        rank, desc = calculate_rank(player_score=10, words_found=5, total_possible=50)
        self.assertIn("Apprentice", rank)


if __name__ == "__main__":
    unittest.main()

