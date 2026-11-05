"""
Boggle scoring rules and performance ranking calculators.
"""
from typing import Tuple

# Official Boggle scoring mapping
BOGGLE_SCORES = {
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    7: 5,
    8: 11  # 8 or more letters
}


def get_word_score(word: str) -> int:
    """Calculate the score for a single word based on official Boggle rules."""
    length = len(word)
    if length < 3:
        return 0
    if length >= 8:
        return 11
    return BOGGLE_SCORES.get(length, 1)


def calculate_rank(player_score: int, words_found: int, total_possible: int) -> Tuple[str, str]:
    """
    Calculate player rank and badge based on score and percentage of words found.
    Returns: (badge_emoji_and_title, short_description)
    """
    pct = (words_found / total_possible * 100) if total_possible > 0 else 0
    
    if pct >= 50 or player_score >= 60:
        return "🏆 Boggle Grandmaster", "Sensational! You found over half the words or scored 60+ points!"
    elif pct >= 30 or player_score >= 35:
        return "⭐ Word Wizard", "Impressive vocabulary and board vision!"
    elif pct >= 15 or player_score >= 15:
        return "✨ Keen Observer", "Good work! Keep spotting those tricky angles."
    else:
        return "🌱 Word Apprentice", "Nice effort! Practice will expand your board awareness."

