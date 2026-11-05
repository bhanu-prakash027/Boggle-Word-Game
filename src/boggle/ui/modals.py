"""
Dialogs and summary modals for Boggle Word Master.
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Callable, List, Optional
from .theme import THEME
from ..models.scoring import get_word_score, calculate_rank


class RoundSummaryModal(tk.Toplevel):
    """Post-round summary dialog showing score, rank badge, and missed words."""

    def __init__(self, parent: tk.Tk, player_score: int, words_found: dict,
                 all_solutions: dict, on_play_again: Callable[[], None],
                 on_inspect_solutions: Callable[[], None]):
        super().__init__(parent)
        self.title("Round Complete - Score Summary")
        self.geometry("490x540")
        self.configure(bg=THEME["bg_card"])
        self.transient(parent)
        self.grab_set()

        total_possible = len(all_solutions)
        max_score = sum(get_word_score(w) for w in all_solutions.keys())
        player_count = len(words_found)
        pct = (player_count / total_possible * 100) if total_possible > 0 else 0
        missed = [w for w in all_solutions.keys() if w.upper() not in words_found]

        rank_title, rank_desc = calculate_rank(player_score, player_count, total_possible)

        # Title
        tk.Label(self, text="ROUND SUMMARY", font=("Segoe UI", 16, "bold"),
                 bg=THEME["bg_card"], fg=THEME["text_primary"]).pack(pady=(16, 4))

        tk.Label(self, text=rank_title, font=("Segoe UI", 14, "bold"),
                 bg=THEME["bg_card"], fg=THEME["accent_amber"]).pack()

        tk.Label(self, text=rank_desc, font=("Segoe UI", 9),
                 bg=THEME["bg_card"], fg=THEME["text_secondary"]).pack(pady=(2, 12))

        # Stats Table
        stats_box = tk.Frame(self, bg=THEME["bg_card_light"], padx=16, pady=12)
        stats_box.pack(fill=tk.X, padx=20, pady=(0, 12))

        rows_data = [
            ("Your Score:", f"{player_score} points"),
            ("Maximum Possible Score:", f"{max_score} points"),
            ("Words Found:", f"{player_count} of {total_possible} ({pct:.1f}%)"),
            ("Longest Word Found:", max(words_found.keys(), key=len, default="None")),
        ]

        for i, (label_txt, val_txt) in enumerate(rows_data):
            tk.Label(stats_box, text=label_txt, font=("Segoe UI", 10),
                     bg=THEME["bg_card_light"], fg=THEME["text_secondary"]).grid(row=i, column=0, sticky="w", pady=2)
            tk.Label(stats_box, text=val_txt, font=("Segoe UI", 10, "bold"),
                     bg=THEME["bg_card_light"], fg=THEME["text_primary"]).grid(row=i, column=1, sticky="e", pady=2, padx=(16, 0))
        stats_box.columnconfigure(1, weight=1)

        # Missed Words Section
        tk.Label(self, text="Top Words You Missed:", font=("Segoe UI", 10, "bold"),
                 bg=THEME["bg_card"], fg=THEME["text_primary"]).pack(anchor="w", padx=22, pady=(0, 4))

        missed_frame = tk.Frame(self, bg=THEME["bg_input"])
        missed_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 14))

        scrollbar = tk.Scrollbar(missed_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        missed_list = tk.Listbox(missed_frame, font=("Consolas", 10), bg=THEME["bg_input"], fg="white",
                                 relief="flat", highlightthickness=0, yscrollcommand=scrollbar.set)
        missed_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.config(command=missed_list.yview)

        missed_sorted = sorted(missed, key=lambda w: (-len(w), w))
        for w in missed_sorted:
            pts = get_word_score(w)
            pts_str = "pt" if pts == 1 else "pts"
            missed_list.insert(tk.END, f"{w.upper():<16} ({pts} {pts_str})")

        # Buttons
        btn_box = tk.Frame(self, bg=THEME["bg_card"])
        btn_box.pack(fill=tk.X, padx=20, pady=(0, 16))

        def handle_solver():
            self.destroy()
            on_inspect_solutions()

        def handle_again():
            self.destroy()
            on_play_again()

        tk.Button(btn_box, text="🔍 Inspect Solutions", font=("Segoe UI", 10),
                  bg=THEME["bg_card_light"], fg=THEME["text_primary"], relief="flat",
                  padx=12, pady=6, cursor="hand2", command=handle_solver).pack(side=tk.LEFT)

        tk.Button(btn_box, text="🎲 Play Again", font=("Segoe UI", 10, "bold"),
                  bg=THEME["accent_emerald"], fg="white", relief="flat",
                  padx=16, pady=6, cursor="hand2", command=handle_again).pack(side=tk.RIGHT)


def ask_custom_grid(parent: tk.Tk, size: int) -> Optional[str]:
    """Prompt user to enter exact letters for a custom Boggle grid."""
    req = size * size
    letters = simpledialog.askstring(
        "Enter Custom Grid",
        f"Enter exactly {req} letters for a {size}x{size} grid:\n(Spaces and punctuation will be ignored)",
        parent=parent
    )
    if letters:
        clean = "".join(c.upper() for c in letters if c.isalpha())
        if len(clean) != req:
            messagebox.showerror(
                "Invalid Length",
                f"You entered {len(clean)} valid letters, but exactly {req} letters are required!"
            )
            return None
        return clean
    return None

