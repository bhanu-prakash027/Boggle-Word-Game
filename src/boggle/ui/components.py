"""
Reusable UI components for Boggle Word Master.
"""
import tkinter as tk
from typing import Callable, Tuple
from .theme import THEME


class LetterTile(tk.Frame):
    """Interactive letter tile supporting hover, click, sequence badge, and path glow."""

    def __init__(self, parent: tk.Widget, row: int, col: int, letter: str,
                 size: int = 52, font_size: int = 18,
                 on_click: Callable[[Tuple[int, int]], None] = None):
        super().__init__(parent, bg=THEME["tile_normal_bg"], width=size, height=size, relief="raised", bd=2)
        self.pack_propagate(False)
        self.pos = (row, col)
        self.letter = letter
        self.font_size = font_size
        self.on_click = on_click

        self.label = tk.Label(self, text=letter, font=("Segoe UI", font_size, "bold"),
                              bg=THEME["tile_normal_bg"], fg=THEME["tile_normal_fg"], cursor="hand2")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.label.bind("<Button-1>", lambda e: self._handle_click())
        self.label.bind("<Enter>", lambda e: self._on_enter())
        self.label.bind("<Leave>", lambda e: self._on_leave())
        self.is_selected = False
        self.is_path = False

    def _handle_click(self):
        if self.on_click:
            self.on_click(self.pos)

    def _on_enter(self):
        if not self.is_selected and not self.is_path:
            self.label.config(bg=THEME["tile_hover_bg"])
            self.config(bg=THEME["tile_hover_bg"])

    def _on_leave(self):
        if not self.is_selected and not self.is_path:
            self.label.config(bg=THEME["tile_normal_bg"])
            self.config(bg=THEME["tile_normal_bg"])

    def set_letter(self, letter: str):
        self.letter = letter
        self.reset()

    def reset(self):
        self.is_selected = False
        self.is_path = False
        self.label.config(text=self.letter, bg=THEME["tile_normal_bg"],
                          fg=THEME["tile_normal_fg"], font=("Segoe UI", self.font_size, "bold"))
        self.config(bg=THEME["tile_normal_bg"])

    def set_selected(self, step: int):
        self.is_selected = True
        self.is_path = False
        bg_col = THEME["accent_amber"] if step == 1 else THEME["accent_blue"]
        self.label.config(text=f"{self.letter}·{step}", bg=bg_col, fg="white", font=("Segoe UI", 12, "bold"))
        self.config(bg=bg_col)

    def set_path_highlight(self, step: int):
        self.is_path = True
        self.is_selected = False
        bg_col = THEME["tile_start_bg"] if step == 1 else THEME["tile_path_bg"]
        self.label.config(text=f"{self.letter} ({step})", bg=bg_col, fg="white", font=("Segoe UI", 11, "bold"))
        self.config(bg=bg_col)

