"""
Boggle board model, dice definitions, and board generator.
"""
import random
from typing import List, Optional

# Classic 16 Boggle Dice faces (4x4)
CLASSIC_DICE_4X4 = [
    "AAEEGN", "ELRTTY", "AOOTTW", "ABBJOO",
    "EHRTVW", "CIMOTU", "DISTTY", "EIOSST",
    "DELRVY", "ACHOPS", "HIMNQU", "EEINSU",
    "EEGHNW", "AFFKPS", "HLNNRZ", "DEILRX"
]

# Deluxe / Big Boggle 25 Dice (5x5)
DELUXE_DICE_5X5 = [
    "AAAFRS", "AAEEEE", "AAFIRS", "ADENNN", "AEEEEM",
    "AEEGMU", "AEGMNN", "AFIRSY", "BJKQXZ", "CCNSTW",
    "CEIILT", "CEILPT", "CEIPST", "DHHNOT", "DHHLOR",
    "DHLNOR", "DDLNOR", "EIIITT", "EMOTTT", "ENSSSU",
    "FIPRSY", "GORRVW", "HIPRRY", "NOOTUW", "OOOTTU"
]

# Frequency weights for general letter distribution (e.g. 3x3)
LETTER_WEIGHTS = {
    'A': 8.5, 'B': 2.0, 'C': 4.0, 'D': 3.8, 'E': 11.2,
    'F': 1.8, 'G': 2.5, 'H': 3.0, 'I': 7.5, 'J': 0.3,
    'K': 1.1, 'L': 5.5, 'M': 3.0, 'N': 6.5, 'O': 7.2,
    'P': 3.1, 'Q': 0.4, 'R': 7.0, 'S': 6.5, 'T': 7.0,
    'U': 4.0, 'V': 1.2, 'W': 1.8, 'X': 0.3, 'Y': 2.5, 'Z': 0.3
}


class Board:
    """Represents a 2D letter grid with dice rolling, custom boards, and letter rearranging."""

    def __init__(self, size: int = 4):
        self.size = size
        self.grid: List[List[str]] = []
        self.generate()

    def generate(self, size: Optional[int] = None) -> List[List[str]]:
        """Roll random dice and balance vowels to generate a rich, solvable board."""
        if size is not None:
            self.size = size

        num_cells = self.size * self.size

        if self.size == 4:
            dice = list(CLASSIC_DICE_4X4)
            random.shuffle(dice)
            letters = [random.choice(die) for die in dice]
        elif self.size == 5:
            dice = list(DELUXE_DICE_5X5)
            random.shuffle(dice)
            letters = [random.choice(die) for die in dice]
        else:
            chars = list(LETTER_WEIGHTS.keys())
            weights = list(LETTER_WEIGHTS.values())
            letters = random.choices(chars, weights=weights, k=num_cells)

        # Balance vowels (ensure at least 20% vowels)
        vowels = set("AEIOU")
        vowel_count = sum(1 for c in letters if c in vowels)
        min_vowels = max(3, num_cells // 5)
        if vowel_count < min_vowels:
            for _ in range(min_vowels - vowel_count):
                idx = random.randint(0, num_cells - 1)
                letters[idx] = random.choice("AEIOU")

        self.grid = [
            letters[i * self.size : (i + 1) * self.size]
            for i in range(self.size)
        ]
        return self.grid

    def shuffle_existing(self) -> List[List[str]]:
        """
        Rearrange/shuffle the existing letters on the board into new positions.
        Preserves the exact same letters, giving the player a fresh perspective.
        """
        if not self.grid:
            return []
        flat = [self.grid[r][c] for r in range(self.size) for c in range(self.size)]
        random.shuffle(flat)
        self.grid = [
            flat[i * self.size : (i + 1) * self.size]
            for i in range(self.size)
        ]
        return self.grid

    def set_custom(self, letters: str, size: int) -> bool:
        """Set board from a string of letters."""
        cleaned = [c.upper() for c in letters if c.isalpha()]
        if len(cleaned) != size * size:
            return False
        self.size = size
        self.grid = [
            cleaned[i * size : (i + 1) * size]
            for i in range(size)
        ]
        return True

    def get_letter(self, row: int, col: int) -> str:
        """Get letter at (row, col)."""
        return self.grid[row][col]

    def is_valid_coord(self, row: int, col: int) -> bool:
        """Check if (row, col) is within grid bounds."""
        return 0 <= row < self.size and 0 <= col < self.size

    def get_all_letters(self) -> List[str]:
        """Return all letters on the board as a flat list."""
        return [self.grid[r][c] for r in range(self.size) for c in range(self.size)]
