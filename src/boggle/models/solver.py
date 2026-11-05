"""
Boggle & Freeform Word Solver with Trie pruning and path tracing.
Supports:
1. "FREEFORM": Words can be formed from ANY letters on the board in any direction or order.
2. "ADJACENT": Classic Boggle rules (orthogonal and diagonal neighbors only).
"""
from collections import Counter
from typing import Dict, List, Optional, Set, Tuple
from .trie import Trie, TrieNode
from .board import Board
from .scoring import get_word_score


class BoggleSolver:
    """
    Solves boards and validates word formations.
    Supports both Freeform (any direction / any tiles on board) and Classic Adjacent modes.
    """

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def __init__(self, board: Board, trie: Optional[Trie] = None, rule_mode: str = "FREEFORM"):
        self.board = board
        self.trie = trie
        self.rule_mode = rule_mode.upper()  # "FREEFORM" or "ADJACENT"
        self.cached_solutions: Dict[str, List[Tuple[int, int]]] = {}

    def set_trie(self, trie: Trie):
        self.trie = trie
        self.cached_solutions.clear()

    def set_rule_mode(self, mode: str):
        mode_upper = mode.upper()
        if mode_upper in ("FREEFORM", "ADJACENT"):
            self.rule_mode = mode_upper
            self.cached_solutions.clear()

    def solve(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Find all valid dictionary words on the board.
        In FREEFORM mode: uses any available tiles on the board.
        In ADJACENT mode: uses 8-directional adjacent tiles.
        """
        if not self.trie or not self.board.grid:
            return {}

        if self.rule_mode == "FREEFORM":
            solutions = self._solve_freeform()
        else:
            solutions = self._solve_adjacent()

        self.cached_solutions = solutions
        return solutions

    def _solve_freeform(self) -> Dict[str, List[Tuple[int, int]]]:
        """Ultra-fast anagram / sub-word solver using Trie branch traversal."""
        found: Dict[str, List[Tuple[int, int]]] = {}

        # Map each character to all its (row, col) positions on the board
        char_positions: Dict[str, List[Tuple[int, int]]] = {}
        counts: Dict[str, int] = Counter()

        for r in range(self.board.size):
            for c in range(self.board.size):
                char = self.board.grid[r][c].lower()
                char_positions.setdefault(char, []).append((r, c))
                counts[char] += 1

        def dfs(node: TrieNode, path_tiles: List[Tuple[int, int]], used_positions: Set[Tuple[int, int]]):
            if node.is_end_of_word and node.word and len(node.word) >= 3:
                if node.word not in found:
                    found[node.word] = list(path_tiles)

            for char, child_node in node.children.items():
                if counts.get(char, 0) > 0:
                    counts[char] -= 1
                    # Assign first available board tile for this character
                    for pos in char_positions[char]:
                        if pos not in used_positions:
                            used_positions.add(pos)
                            path_tiles.append(pos)
                            dfs(child_node, path_tiles, used_positions)
                            path_tiles.pop()
                            used_positions.remove(pos)
                            break
                    counts[char] += 1

        dfs(self.trie.root, [], set())
        return found

    def _solve_adjacent(self) -> Dict[str, List[Tuple[int, int]]]:
        """Classic Boggle 8-direction adjacent DFS solver with branch pruning."""
        found: Dict[str, List[Tuple[int, int]]] = {}
        rows = self.board.size
        cols = self.board.size

        def dfs(r: int, c: int, node: TrieNode, visited: Set[Tuple[int, int]], path: List[Tuple[int, int]]):
            if node.is_end_of_word and node.word and len(node.word) >= 3:
                if node.word not in found:
                    found[node.word] = list(path)

            for dr, dc in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    char = self.board.grid[nr][nc].lower()
                    if char in node.children:
                        visited.add((nr, nc))
                        path.append((nr, nc))
                        dfs(nr, nc, node.children[char], visited, path)
                        path.pop()
                        visited.remove((nr, nc))

        for r in range(rows):
            for c in range(cols):
                start_char = self.board.grid[r][c].lower()
                if start_char in self.trie.root.children:
                    start_node = self.trie.root.children[start_char]
                    visited = {(r, c)}
                    path = [(r, c)]
                    dfs(r, c, start_node, visited, path)

        return found

    def find_path(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Find tile coordinates for a word based on current rule mode."""
        clean = word.strip().lower()
        if not clean or not self.board.grid:
            return None

        if clean in self.cached_solutions:
            return self.cached_solutions[clean]

        if self.rule_mode == "FREEFORM":
            return self._find_path_freeform(clean)
        else:
            return self._find_path_adjacent(clean)

    def _find_path_freeform(self, clean: str) -> Optional[List[Tuple[int, int]]]:
        """Check if board has enough tiles to form word and return matching positions."""
        available_positions: Dict[str, List[Tuple[int, int]]] = {}
        for r in range(self.board.size):
            for c in range(self.board.size):
                char = self.board.grid[r][c].lower()
                available_positions.setdefault(char, []).append((r, c))

        path: List[Tuple[int, int]] = []
        used: Set[Tuple[int, int]] = set()

        for char in clean:
            found_tile = False
            for pos in available_positions.get(char, []):
                if pos not in used:
                    used.add(pos)
                    path.append(pos)
                    found_tile = True
                    break
            if not found_tile:
                return None  # Missing letter on board

        return path

    def _find_path_adjacent(self, clean: str) -> Optional[List[Tuple[int, int]]]:
        """Classic adjacent DFS path finder."""
        rows = self.board.size
        cols = self.board.size

        def dfs(r: int, c: int, idx: int, visited: Set[Tuple[int, int]], path: List[Tuple[int, int]]) -> bool:
            if idx == len(clean):
                return True

            for dr, dc in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    if self.board.grid[nr][nc].lower() == clean[idx]:
                        visited.add((nr, nc))
                        path.append((nr, nc))
                        if dfs(nr, nc, idx + 1, visited, path):
                            return True
                        path.pop()
                        visited.remove((nr, nc))
            return False

        first = clean[0]
        for r in range(rows):
            for c in range(cols):
                if self.board.grid[r][c].lower() == first:
                    visited = {(r, c)}
                    path = [(r, c)]
                    if dfs(r, c, 1, visited, path):
                        return path
        return None

    def validate(self, word: str) -> Tuple[bool, str, Optional[List[Tuple[int, int]]]]:
        """Validate word against length, board letter availability, and dictionary."""
        clean = word.strip().lower()
        if len(clean) < 3:
            return False, "Minimum length is 3 letters!", None

        path = self.find_path(clean)
        if not path:
            if self.rule_mode == "FREEFORM":
                return False, "Letters not available on the board!", None
            else:
                return False, "Word cannot be formed by adjacent tiles!", None

        if not self.trie or not self.trie.contains(clean):
            return False, f"'{word.upper()}' is not in the dictionary!", None

        score = get_word_score(clean)
        pts_str = "point" if score == 1 else "points"
        return True, f"+{score} {pts_str}!", path
