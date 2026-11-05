"""
Main Boggle Word Master Application window and coordinator.
Supports selecting and rearranging ANY letters on the board in ANY order (non-adjacent).
Includes:
- Interactive Word Tray showing selected letter tiles in chosen order
- "Rearrange Board" (shuffle existing letters on the grid for fresh perspective)
- "New Letters" (roll brand new dice)
- Keyboard and click dual-input with instant dictionary validation
"""
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional, Tuple

from .theme import THEME
from .components import LetterTile
from .modals import RoundSummaryModal, ask_custom_grid
from ..models.board import Board
from ..models.solver import BoggleSolver
from ..models.trie import Trie
from ..models.scoring import get_word_score
from ..utils.audio import SoundManager
from ..utils.downloader import download_enable_dictionary


class BoggleApp:
    """Main Application Controller and View."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Word Master - Freeform Letter Game & Solver")
        self.root.geometry("1080x800")
        self.root.minsize(960, 720)
        self.root.configure(bg=THEME["bg_main"])

        # Models & State
        self.grid_size = 4
        self.rule_mode = "FREEFORM"  # Default: ANY order, any letters anywhere!
        self.board = Board(size=self.grid_size)
        self.solver = BoggleSolver(board=self.board, rule_mode=self.rule_mode)
        self.sound = SoundManager(enabled=True)
        self.trie: Optional[Trie] = None

        # Game Play State
        self.game_mode = "PLAY"  # "PLAY" or "SOLVER"
        self.time_limit = 120    # Seconds (0 = Untimed)
        self.time_left = self.time_limit
        self.is_playing = False
        self.is_paused = False
        self.timer_after_id = None
        self.player_score = 0
        self.player_words: Dict[str, int] = {}  # word -> score

        # Tile Selection & Highlights
        self.selected_path: List[Tuple[int, int]] = []
        self.tiles: List[List[LetterTile]] = []
        self.active_highlight: List[Tuple[int, int]] = []
        self.highlight_after_id = None

        # UI Build
        self._setup_styles()
        self._build_header()
        self._build_main_layout()
        self._build_status_bar()
        self._setup_bindings()

        # Load Dictionary & Initialize Board
        self._init_dictionary()
        self.start_new_game()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=THEME["bg_main"])
        style.configure("Card.TFrame", background=THEME["bg_card"])
        style.configure("TLabel", background=THEME["bg_card"], foreground=THEME["text_primary"])
        style.configure("Vertical.TScrollbar", background=THEME["bg_card_light"], arrowcolor=THEME["text_primary"])

    def _setup_bindings(self):
        self.root.bind("<Escape>", lambda e: self.clear_selection())
        self.root.bind("<BackSpace>", self._on_backspace_pressed)
        self.word_entry.focus_set()

    def _on_backspace_pressed(self, event=None):
        # If entry is empty but we have tiles selected in tray, pop one tile
        if self.word_entry.get() == "" and self.selected_path:
            self.selected_path.pop()
            self._update_tile_states()
            self._update_tray_and_entry()

    # -------------------------------------------------------------
    # Layout Builders
    # -------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=THEME["bg_card"], height=65, padx=20, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)

        title_box = tk.Frame(header, bg=THEME["bg_card"])
        title_box.pack(side=tk.LEFT)

        tk.Label(title_box, text="🔠 WORD MASTER", font=("Segoe UI", 20, "bold"),
                 bg=THEME["bg_card"], fg=THEME["accent_emerald"]).pack(side=tk.LEFT)
        tk.Label(title_box, text="ANY DIRECTION", font=("Segoe UI", 10, "bold"),
                 bg=THEME["bg_card"], fg=THEME["accent_amber"], padx=8).pack(side=tk.LEFT, pady=(5, 0))

        btn_box = tk.Frame(header, bg=THEME["bg_card"])
        btn_box.pack(side=tk.RIGHT)

        self.play_mode_btn = tk.Button(btn_box, text="🎮 Play Mode", font=("Segoe UI", 10, "bold"),
                                       bg=THEME["accent_blue"], fg="white", activebackground=THEME["accent_blue"],
                                       relief="flat", padx=12, pady=5, cursor="hand2", command=self._set_play_mode)
        self.play_mode_btn.pack(side=tk.LEFT, padx=4)

        self.solver_mode_btn = tk.Button(btn_box, text="🔍 Solver Mode", font=("Segoe UI", 10),
                                         bg=THEME["bg_card_light"], fg=THEME["text_primary"],
                                         relief="flat", padx=12, pady=5, cursor="hand2", command=self._set_solver_mode)
        self.solver_mode_btn.pack(side=tk.LEFT, padx=4)

        dict_btn = tk.Button(btn_box, text="📚 Dictionary", font=("Segoe UI", 10),
                             bg=THEME["bg_card_light"], fg=THEME["text_primary"],
                             relief="flat", padx=10, pady=5, cursor="hand2", command=self._show_dictionary_menu)
        dict_btn.pack(side=tk.LEFT, padx=4)

        sound_icon = "🔊" if self.sound.enabled else "🔇"
        self.sound_btn = tk.Button(btn_box, text=sound_icon, font=("Segoe UI", 11),
                                   bg=THEME["bg_card_light"], fg=THEME["text_primary"],
                                   relief="flat", padx=8, pady=4, cursor="hand2", command=self._toggle_sound)
        self.sound_btn.pack(side=tk.LEFT, padx=4)

    def _build_main_layout(self):
        container = tk.Frame(self.root, bg=THEME["bg_main"], padx=15, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        # Left Column: Board & Input
        left_col = tk.Frame(container, bg=THEME["bg_main"])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Controls bar
        controls_card = tk.Frame(left_col, bg=THEME["bg_card"], padx=12, pady=8)
        controls_card.pack(fill=tk.X, pady=(0, 10))

        new_btn = tk.Button(controls_card, text="🎲 New Letters", font=("Segoe UI", 10, "bold"),
                            bg=THEME["accent_emerald"], fg="white", relief="flat", padx=10, pady=4,
                            cursor="hand2", command=self.start_new_game)
        new_btn.pack(side=tk.LEFT, padx=(0, 6))

        # REARRANGE / SHUFFLE EXISTING LETTERS BUTTON
        rearrange_btn = tk.Button(controls_card, text="🔀 Rearrange Board", font=("Segoe UI", 10, "bold"),
                                  bg=THEME["accent_purple"], fg="white", relief="flat", padx=10, pady=4,
                                  cursor="hand2", command=self.rearrange_current_board)
        rearrange_btn.pack(side=tk.LEFT, padx=(0, 8))

        # Rules Dropdown: Freeform vs Adjacent
        tk.Label(controls_card, text="Rule:", font=("Segoe UI", 9, "bold"),
                 bg=THEME["bg_card"], fg=THEME["accent_amber"]).pack(side=tk.LEFT, padx=(4, 2))
        self.rule_var = tk.StringVar(value="Any Letters / Any Order")
        rule_combo = ttk.Combobox(controls_card, textvariable=self.rule_var,
                                  values=["Any Letters / Any Order", "Classic (Adjacent Only)"],
                                  state="readonly", width=22, font=("Segoe UI", 9))
        rule_combo.pack(side=tk.LEFT, padx=(0, 8))
        rule_combo.bind("<<ComboboxSelected>>", self._on_rule_change)

        # Grid size selector
        tk.Label(controls_card, text="Size:", font=("Segoe UI", 9),
                 bg=THEME["bg_card"], fg=THEME["text_secondary"]).pack(side=tk.LEFT, padx=(4, 2))
        self.size_var = tk.StringVar(value="4x4 (16 Letters)")
        size_combo = ttk.Combobox(controls_card, textvariable=self.size_var,
                                  values=["3x3 (9 Letters)", "4x4 (16 Letters)", "5x5 (25 Letters)"],
                                  state="readonly", width=14, font=("Segoe UI", 9))
        size_combo.pack(side=tk.LEFT, padx=(0, 8))
        size_combo.bind("<<ComboboxSelected>>", self._on_size_change)

        # Timer selector
        self.timer_label_ui = tk.Label(controls_card, text="Time:", font=("Segoe UI", 9),
                                       bg=THEME["bg_card"], fg=THEME["text_secondary"])
        self.timer_label_ui.pack(side=tk.LEFT, padx=(4, 2))
        self.timer_var = tk.StringVar(value="2 Min")
        self.timer_combo = ttk.Combobox(controls_card, textvariable=self.timer_var,
                                        values=["1 Min (60s)", "2 Min (120s)", "3 Min (180s)", "Untimed (Zen)"],
                                        state="readonly", width=12, font=("Segoe UI", 9))
        self.timer_combo.pack(side=tk.LEFT, padx=(0, 8))
        self.timer_combo.bind("<<ComboboxSelected>>", self._on_timer_option_change)

        custom_btn = tk.Button(controls_card, text="✏️ Custom", font=("Segoe UI", 9),
                               bg=THEME["bg_card_light"], fg=THEME["text_primary"], relief="flat",
                               padx=8, pady=4, cursor="hand2", command=self._enter_custom_grid)
        custom_btn.pack(side=tk.RIGHT)

        # Board container
        self.board_card = tk.Frame(left_col, bg=THEME["bg_card"], padx=16, pady=12)
        self.board_card.pack(fill=tk.BOTH, expand=True)

        self.grid_container = tk.Frame(self.board_card, bg=THEME["bg_card"])
        self.grid_container.pack(expand=True)

        # Visual Word Tray (Selected Letters Staging Area)
        self.tray_frame = tk.Frame(left_col, bg=THEME["bg_card"], padx=15, pady=8)
        self.tray_frame.pack(fill=tk.X, pady=(10, 0))

        tray_header = tk.Frame(self.tray_frame, bg=THEME["bg_card"])
        tray_header.pack(fill=tk.X, pady=(0, 4))

        tk.Label(tray_header, text="SELECTED LETTERS TRAY (IN ORDER):", font=("Segoe UI", 8, "bold"),
                 bg=THEME["bg_card"], fg=THEME["text_secondary"]).pack(side=tk.LEFT)

        self.tray_tiles_container = tk.Frame(self.tray_frame, bg=THEME["bg_input"], height=48, padx=8, pady=6)
        self.tray_tiles_container.pack(fill=tk.X)
        self.tray_tiles_container.pack_propagate(False)

        # Input row
        input_card = tk.Frame(left_col, bg=THEME["bg_card"], padx=15, pady=8)
        input_card.pack(fill=tk.X, pady=(6, 0))

        input_row = tk.Frame(input_card, bg=THEME["bg_card"])
        input_row.pack(fill=tk.X)

        tk.Label(input_row, text="Word:", font=("Segoe UI", 11, "bold"),
                 bg=THEME["bg_card"], fg=THEME["text_primary"]).pack(side=tk.LEFT, padx=(0, 8))

        self.word_entry = tk.Entry(input_row, font=("Segoe UI", 14, "bold"), bg=THEME["bg_input"], fg="white",
                                   insertbackground="white", relief="flat", highlightthickness=1,
                                   highlightbackground=THEME["accent_blue"], width=16)
        self.word_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=4)
        self.word_entry.bind("<Return>", lambda e: self.submit_current_word())
        self.word_entry.bind("<KeyRelease>", self._on_word_entry_typing)

        submit_btn = tk.Button(input_row, text="Submit ↵", font=("Segoe UI", 10, "bold"),
                               bg=THEME["accent_blue"], fg="white", relief="flat", padx=16, pady=6,
                               cursor="hand2", command=self.submit_current_word)
        submit_btn.pack(side=tk.LEFT, padx=(0, 6))

        clear_btn = tk.Button(input_row, text="Clear ✕", font=("Segoe UI", 10),
                              bg=THEME["bg_card_light"], fg=THEME["text_primary"], relief="flat",
                              padx=12, pady=6, cursor="hand2", command=self.clear_selection)
        clear_btn.pack(side=tk.LEFT)

        self.message_banner = tk.Label(input_card,
                                       text="✨ Click any letters anywhere on the board or type on your keyboard to create meaningful words!",
                                       font=("Segoe UI", 9), bg=THEME["bg_card"], fg=THEME["accent_emerald"])
        self.message_banner.pack(fill=tk.X, pady=(4, 0))

        # Right Column: Dashboards
        self.right_col = tk.Frame(container, bg=THEME["bg_card"], width=360, padx=16, pady=16)
        self.right_col.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_col.pack_propagate(False)

        self._build_play_dashboard()
        self._build_solver_dashboard()

    def _build_play_dashboard(self):
        self.play_panel = tk.Frame(self.right_col, bg=THEME["bg_card"])
        self.play_panel.pack(fill=tk.BOTH, expand=True)

        stats_frame = tk.Frame(self.play_panel, bg=THEME["bg_card"])
        stats_frame.pack(fill=tk.X, pady=(0, 12))

        timer_box = tk.Frame(stats_frame, bg=THEME["bg_card_light"], padx=12, pady=8)
        timer_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        tk.Label(timer_box, text="TIME REMAINING", font=("Segoe UI", 8, "bold"),
                 bg=THEME["bg_card_light"], fg=THEME["text_secondary"]).pack()
        self.timer_display = tk.Label(timer_box, text="02:00", font=("Segoe UI", 24, "bold"),
                                      bg=THEME["bg_card_light"], fg=THEME["accent_amber"])
        self.timer_display.pack()

        score_box = tk.Frame(stats_frame, bg=THEME["bg_card_light"], padx=12, pady=8)
        score_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
        tk.Label(score_box, text="YOUR SCORE", font=("Segoe UI", 8, "bold"),
                 bg=THEME["bg_card_light"], fg=THEME["text_secondary"]).pack()
        self.score_display = tk.Label(score_box, text="0", font=("Segoe UI", 24, "bold"),
                                      bg=THEME["bg_card_light"], fg=THEME["accent_emerald"])
        self.score_display.pack()

        list_header = tk.Frame(self.play_panel, bg=THEME["bg_card"])
        list_header.pack(fill=tk.X, pady=(4, 6))
        self.words_count_lbl = tk.Label(list_header, text="Words Found (0)", font=("Segoe UI", 11, "bold"),
                                        bg=THEME["bg_card"], fg=THEME["text_primary"])
        self.words_count_lbl.pack(side=tk.LEFT)

        list_frame = tk.Frame(self.play_panel, bg=THEME["bg_input"], relief="flat")
        list_frame.pack(fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.player_word_listbox = tk.Listbox(list_frame, font=("Consolas", 11),
                                              bg=THEME["bg_input"], fg="white", selectbackground=THEME["accent_blue"],
                                              relief="flat", highlightthickness=0, yscrollcommand=scroll.set)
        self.player_word_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scroll.config(command=self.player_word_listbox.yview)
        self.player_word_listbox.bind("<<ListboxSelect>>", self._on_player_word_selected)

        bottom_play_btns = tk.Frame(self.play_panel, bg=THEME["bg_card"])
        bottom_play_btns.pack(fill=tk.X, pady=(10, 0))

        self.pause_btn = tk.Button(bottom_play_btns, text="⏸ Pause", font=("Segoe UI", 9),
                                   bg=THEME["bg_card_light"], fg=THEME["text_primary"], relief="flat",
                                   padx=10, pady=4, cursor="hand2", command=self._toggle_pause)
        self.pause_btn.pack(side=tk.LEFT)

        finish_btn = tk.Button(bottom_play_btns, text="End Round & Solve", font=("Segoe UI", 9, "bold"),
                               bg=THEME["accent_rose"], fg="white", relief="flat",
                               padx=12, pady=4, cursor="hand2", command=self._end_round)
        finish_btn.pack(side=tk.RIGHT)

    def _build_solver_dashboard(self):
        self.solver_panel = tk.Frame(self.right_col, bg=THEME["bg_card"])

        stats_frame = tk.Frame(self.solver_panel, bg=THEME["bg_card_light"], padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.solver_stats_lbl = tk.Label(stats_frame, text="Total: 0 words | Max: 0 pts",
                                         font=("Segoe UI", 11, "bold"),
                                         bg=THEME["bg_card_light"], fg=THEME["accent_emerald"])
        self.solver_stats_lbl.pack()

        filter_box = tk.Frame(self.solver_panel, bg=THEME["bg_card"])
        filter_box.pack(fill=tk.X, pady=(0, 8))

        tk.Label(filter_box, text="Filter:", font=("Segoe UI", 9),
                 bg=THEME["bg_card"], fg=THEME["text_secondary"]).pack(side=tk.LEFT, padx=(0, 4))
        self.filter_entry = tk.Entry(filter_box, font=("Segoe UI", 10), bg=THEME["bg_input"], fg="white",
                                     relief="flat", highlightthickness=1, highlightbackground=THEME["bg_card_light"])
        self.filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.filter_entry.bind("<KeyRelease>", lambda e: self._refresh_solver_list())

        self.min_len_var = tk.StringVar(value="All Lengths")
        len_combo = ttk.Combobox(filter_box, textvariable=self.min_len_var,
                                 values=["All Lengths", "3+ Letters", "4+ Letters", "5+ Letters", "6+ Letters", "7+ Letters"],
                                 state="readonly", width=11, font=("Segoe UI", 8))
        len_combo.pack(side=tk.RIGHT)
        len_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_solver_list())

        sol_frame = tk.Frame(self.solver_panel, bg=THEME["bg_input"], relief="flat")
        sol_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(sol_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.solver_word_listbox = tk.Listbox(sol_frame, font=("Consolas", 10),
                                              bg=THEME["bg_input"], fg="white", selectbackground=THEME["accent_emerald"],
                                              relief="flat", highlightthickness=0, yscrollcommand=scrollbar.set)
        self.solver_word_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.config(command=self.solver_word_listbox.yview)
        self.solver_word_listbox.bind("<<ListboxSelect>>", self._on_solver_word_selected)

        tk.Label(self.solver_panel, text="💡 Click any word to highlight its letters on the board!",
                 font=("Segoe UI", 8), bg=THEME["bg_card"], fg=THEME["accent_amber"], pady=4).pack(fill=tk.X)

    def _build_status_bar(self):
        status_bar = tk.Frame(self.root, bg=THEME["bg_status"], height=28, padx=15, pady=4)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.dict_status_lbl = tk.Label(status_bar, text="Dictionary: Loading...", font=("Segoe UI", 8),
                                        bg=THEME["bg_status"], fg=THEME["text_secondary"])
        self.dict_status_lbl.pack(side=tk.LEFT)

        self.rule_status_lbl = tk.Label(status_bar, text="Mode: Any Letters / Any Order", font=("Segoe UI", 8, "bold"),
                                        bg=THEME["bg_status"], fg=THEME["accent_amber"])
        self.rule_status_lbl.pack(side=tk.LEFT, padx=20)

        self.speed_status_lbl = tk.Label(status_bar, text="Ready", font=("Segoe UI", 8),
                                         bg=THEME["bg_status"], fg=THEME["text_secondary"])
        self.speed_status_lbl.pack(side=tk.RIGHT)

    # -------------------------------------------------------------
    # Board Rendering & Interactive Selection
    # -------------------------------------------------------------
    def _render_board(self):
        for w in self.grid_container.winfo_children():
            w.destroy()

        self.tiles = []
        rows = self.grid_size
        cols = self.grid_size

        tile_size = 64 if rows == 3 else (52 if rows == 4 else 44)
        font_size = 22 if rows == 3 else (18 if rows == 4 else 15)

        for r in range(rows):
            row_tiles = []
            for c in range(cols):
                letter = self.board.get_letter(r, c)
                tile = LetterTile(
                    parent=self.grid_container,
                    row=r,
                    col=c,
                    letter=letter,
                    size=tile_size,
                    font_size=font_size,
                    on_click=self._on_tile_clicked
                )
                tile.grid(row=r, column=c, padx=4, pady=4)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def _on_tile_clicked(self, pos: Tuple[int, int]):
        r, c = pos
        if self.is_paused:
            self._toggle_pause()

        # If clicking the last tile -> Undo / remove it
        if self.selected_path and self.selected_path[-1] == pos:
            self.selected_path.pop()
            self._update_tile_states()
            self._update_tray_and_entry()
            return

        # If clicking an earlier tile in current selection -> truncate back to that tile
        if pos in self.selected_path:
            idx = self.selected_path.index(pos)
            self.selected_path = self.selected_path[:idx + 1]
            self._update_tile_states()
            self._update_tray_and_entry()
            return

        # Check adjacency ONLY if in Classic Adjacent mode
        if self.rule_mode == "ADJACENT":
            if self.selected_path:
                lr, lc = self.selected_path[-1]
                if max(abs(r - lr), abs(c - lc)) > 1:
                    self.selected_path = [pos]
                else:
                    self.selected_path.append(pos)
            else:
                self.selected_path = [pos]
        else:
            # FREEFORM MODE: Any tile anywhere on the board in any direction or order!
            self.selected_path.append(pos)

        self._update_tile_states()
        self._update_tray_and_entry()

    def _update_tile_states(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()

        if self.active_highlight:
            for step, (r, c) in enumerate(self.active_highlight, start=1):
                self.tiles[r][c].set_path_highlight(step)
            return

        for step, (r, c) in enumerate(self.selected_path, start=1):
            self.tiles[r][c].set_selected(step)

    def _update_tray_and_entry(self):
        # Update text entry
        word = "".join(self.board.get_letter(r, c) for r, c in self.selected_path)
        self.word_entry.delete(0, tk.END)
        self.word_entry.insert(0, word)

        # Update Visual Word Tray
        for w in self.tray_tiles_container.winfo_children():
            w.destroy()

        if not self.selected_path:
            tk.Label(self.tray_tiles_container, text="[ Tray empty - Click board letters to pick them ]",
                     font=("Segoe UI", 9, "italic"), bg=THEME["bg_input"], fg=THEME["text_muted"]).pack(side=tk.LEFT, pady=6)
            return

        for idx, (r, c) in enumerate(self.selected_path):
            letter = self.board.get_letter(r, c)
            badge_frame = tk.Frame(self.tray_tiles_container, bg=THEME["accent_blue"], padx=6, pady=2, relief="raised", bd=1)
            badge_frame.pack(side=tk.LEFT, padx=3)
            
            lbl = tk.Label(badge_frame, text=f"{letter}", font=("Segoe UI", 12, "bold"),
                           bg=THEME["accent_blue"], fg="white", cursor="hand2")
            lbl.pack(side=tk.LEFT)
            
            # Click letter in tray to remove it
            lbl.bind("<Button-1>", lambda e, p=(r, c): self._on_tray_tile_clicked(p))

    def _on_tray_tile_clicked(self, pos: Tuple[int, int]):
        if pos in self.selected_path:
            self.selected_path.remove(pos)
            self._update_tile_states()
            self._update_tray_and_entry()

    def _on_word_entry_typing(self, event=None):
        typed = self.word_entry.get().strip().upper()
        path = self.solver.find_path(typed)
        if path:
            self.selected_path = path
            self._update_tile_states()
            self._update_tray_from_path()
        else:
            self.selected_path = []
            self._update_tile_states()
            self._update_tray_from_path()

    def _update_tray_from_path(self):
        for w in self.tray_tiles_container.winfo_children():
            w.destroy()

        if not self.selected_path:
            tk.Label(self.tray_tiles_container, text="[ Tray empty - Click board letters to pick them ]",
                     font=("Segoe UI", 9, "italic"), bg=THEME["bg_input"], fg=THEME["text_muted"]).pack(side=tk.LEFT, pady=6)
            return

        for idx, (r, c) in enumerate(self.selected_path):
            letter = self.board.get_letter(r, c)
            badge_frame = tk.Frame(self.tray_tiles_container, bg=THEME["accent_blue"], padx=6, pady=2, relief="raised", bd=1)
            badge_frame.pack(side=tk.LEFT, padx=3)
            lbl = tk.Label(badge_frame, text=f"{letter}", font=("Segoe UI", 12, "bold"),
                           bg=THEME["accent_blue"], fg="white", cursor="hand2")
            lbl.pack(side=tk.LEFT)
            lbl.bind("<Button-1>", lambda e, p=(r, c): self._on_tray_tile_clicked(p))

    def clear_selection(self):
        self.selected_path.clear()
        self.active_highlight.clear()
        if self.highlight_after_id:
            self.root.after_cancel(self.highlight_after_id)
            self.highlight_after_id = None
        self.word_entry.delete(0, tk.END)
        self._update_tile_states()
        self._update_tray_and_entry()
        self.word_entry.focus_set()

    # -------------------------------------------------------------
    # Rearrange & Shuffle Features
    # -------------------------------------------------------------
    def rearrange_current_board(self):
        """Rearrange/shuffle the existing letters on the grid without rolling new ones."""
        self.board.shuffle_existing()
        self.solver.cached_solutions.clear()
        self._render_board()
        self.clear_selection()
        self.sound.play("tick")
        self.message_banner.config(text="🔀 Board rearranged! Spot new words with this fresh layout.", fg=THEME["accent_purple"])
        if self.game_mode == "SOLVER":
            self.solve_current_board()

    def _on_rule_change(self, event=None):
        sel = self.rule_var.get()
        if "Classic" in sel:
            self.rule_mode = "ADJACENT"
            self.rule_status_lbl.config(text="Mode: Classic (Adjacent Only)", fg=THEME["accent_blue"])
            self.message_banner.config(text="🧭 Classic Mode: Select adjacent tiles (orthogonal or diagonal)!",
                                       fg=THEME["accent_blue"])
        else:
            self.rule_mode = "FREEFORM"
            self.rule_status_lbl.config(text="Mode: Any Letters / Any Order", fg=THEME["accent_amber"])
            self.message_banner.config(text="✨ Any Order Mode: Select ANY letters anywhere on the board!",
                                       fg=THEME["accent_emerald"])

        self.solver.set_rule_mode(self.rule_mode)
        self.clear_selection()
        if self.game_mode == "SOLVER":
            self.solve_current_board()

    # -------------------------------------------------------------
    # Game Loop & Timer
    # -------------------------------------------------------------
    def start_new_game(self):
        self.board.generate(self.grid_size)
        self.solver.cached_solutions.clear()
        self._render_board()
        self.clear_selection()

        self.player_score = 0
        self.player_words.clear()
        self.player_word_listbox.delete(0, tk.END)
        self.score_display.config(text="0")
        self.words_count_lbl.config(text="Words Found (0)")

        mode_tip = "Select ANY letters anywhere on the board in ANY order!" if self.rule_mode == "FREEFORM" else "Select adjacent tiles!"
        self.message_banner.config(text=f"New letters rolled! {mode_tip}", fg=THEME["accent_emerald"])

        if self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        self.time_left = self.time_limit
        self.is_playing = True
        self.is_paused = False
        self.pause_btn.config(text="⏸ Pause")

        if self.game_mode == "PLAY":
            if self.time_limit > 0:
                self._update_timer_display()
                self._schedule_timer_tick()
            else:
                self.timer_display.config(text="ZEN", fg=THEME["accent_emerald"])
        else:
            self.solve_current_board()

    def _schedule_timer_tick(self):
        if self.is_playing and not self.is_paused and self.time_limit > 0:
            self.timer_after_id = self.root.after(1000, self._on_timer_tick)

    def _on_timer_tick(self):
        if not self.is_playing or self.is_paused:
            return
        self.time_left -= 1
        self._update_timer_display()

        if 0 < self.time_left <= 5:
            self.sound.play("tick")

        if self.time_left <= 0:
            self._on_time_up()
        else:
            self._schedule_timer_tick()

    def _update_timer_display(self):
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.timer_display.config(text=f"{mins:02d}:{secs:02d}")
        if self.time_left <= 10:
            self.timer_display.config(fg=THEME["accent_rose"])
        elif self.time_left <= 30:
            self.timer_display.config(fg=THEME["accent_amber"])
        else:
            self.timer_display.config(fg=THEME["accent_emerald"])

    def _toggle_pause(self):
        if not self.is_playing:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.config(text="▶ Resume")
            self.message_banner.config(text="Game Paused", fg=THEME["accent_amber"])
        else:
            self.pause_btn.config(text="⏸ Pause")
            self.message_banner.config(text="Game Resumed!", fg=THEME["accent_emerald"])
            self._schedule_timer_tick()

    def _on_time_up(self):
        self.is_playing = False
        self.sound.play("game_over")
        self.message_banner.config(text="Time's Up! Round finished.", fg=THEME["accent_rose"])
        self._show_round_summary()

    def _end_round(self):
        if messagebox.askyesno("Finish Round", "End this round and see all solutions?"):
            self.is_playing = False
            if self.timer_after_id:
                self.root.after_cancel(self.timer_after_id)
                self.timer_after_id = None
            self._show_round_summary()

    def submit_current_word(self):
        word = self.word_entry.get().strip().upper()
        if not word:
            return

        if word in self.player_words:
            self.sound.play("error")
            self.message_banner.config(text=f"'{word}' was already found!", fg=THEME["accent_amber"])
            self.clear_selection()
            return

        is_valid, msg, path = self.solver.validate(word)
        if is_valid:
            score = get_word_score(word.lower())
            self.player_words[word] = score
            self.player_score += score
            self.sound.play("success")
            self.message_banner.config(text=f"✓ '{word}' — {msg}", fg=THEME["accent_emerald"])

            self.score_display.config(text=str(self.player_score))
            self.words_count_lbl.config(text=f"Words Found ({len(self.player_words)})")
            pts_str = f"+{score} pt" if score == 1 else f"+{score} pts"
            self.player_word_listbox.insert(0, f"{word:<14} {pts_str:>8}")
            self.clear_selection()
        else:
            self.sound.play("error")
            self.message_banner.config(text=f"✕ {msg}", fg=THEME["accent_rose"])

    def _on_player_word_selected(self, event=None):
        sel = self.player_word_listbox.curselection()
        if not sel:
            return
        word = self.player_word_listbox.get(sel[0]).split()[0].lower()
        path = self.solver.find_path(word)
        if path:
            self._highlight_path_on_board(path)

    # -------------------------------------------------------------
    # Solver Mode
    # -------------------------------------------------------------
    def _set_play_mode(self):
        self.game_mode = "PLAY"
        self.play_mode_btn.config(bg=THEME["accent_blue"], fg="white", font=("Segoe UI", 10, "bold"))
        self.solver_mode_btn.config(bg=THEME["bg_card_light"], fg=THEME["text_primary"], font=("Segoe UI", 10))
        self.solver_panel.pack_forget()
        self.play_panel.pack(fill=tk.BOTH, expand=True)
        self.timer_label_ui.pack(side=tk.LEFT, padx=(4, 2))
        self.timer_combo.pack(side=tk.LEFT, padx=(0, 8))
        self.clear_selection()

    def _set_solver_mode(self):
        self.game_mode = "SOLVER"
        self.solver_mode_btn.config(bg=THEME["accent_blue"], fg="white", font=("Segoe UI", 10, "bold"))
        self.play_mode_btn.config(bg=THEME["bg_card_light"], fg=THEME["text_primary"], font=("Segoe UI", 10))
        self.play_panel.pack_forget()
        self.solver_panel.pack(fill=tk.BOTH, expand=True)
        self.timer_label_ui.pack_forget()
        self.timer_combo.pack_forget()
        self.solve_current_board()

    def solve_current_board(self):
        if not self.trie:
            return
        t0 = time.time()
        solutions = self.solver.solve()
        t1 = time.time()
        ms = (t1 - t0) * 1000

        total = len(solutions)
        max_pts = sum(get_word_score(w) for w in solutions.keys())
        mode_name = "Any Letters / Any Order" if self.rule_mode == "FREEFORM" else "Adjacent"
        self.solver_stats_lbl.config(text=f"Mode: {mode_name} | Total: {total} words | Max: {max_pts} pts | In {ms:.2f}ms")
        self.speed_status_lbl.config(text=f"Solver: {ms:.2f}ms ({total} words)")
        self._refresh_solver_list()

    def _refresh_solver_list(self):
        self.solver_word_listbox.delete(0, tk.END)
        filter_text = self.filter_entry.get().strip().lower()
        sel = self.min_len_var.get()
        min_len = 3
        if "4+" in sel: min_len = 4
        elif "5+" in sel: min_len = 5
        elif "6+" in sel: min_len = 6
        elif "7+" in sel: min_len = 7

        sorted_words = sorted(self.solver.cached_solutions.keys(), key=lambda w: (-len(w), w))
        current_len = None
        for w in sorted_words:
            if len(w) < min_len or (filter_text and filter_text not in w):
                continue
            if len(w) != current_len:
                current_len = len(w)
                pts = get_word_score(w)
                self.solver_word_listbox.insert(tk.END, f"--- {current_len} LETTERS ({pts} pts each) ---")
            pts = get_word_score(w)
            pts_str = "pt" if pts == 1 else "pts"
            self.solver_word_listbox.insert(tk.END, f"  {w.upper():<16} {pts:>2} {pts_str}")

    def _on_solver_word_selected(self, event=None):
        sel = self.solver_word_listbox.curselection()
        if not sel:
            return
        txt = self.solver_word_listbox.get(sel[0]).strip()
        if txt.startswith("---"):
            return
        word = txt.split()[0].lower()
        path = self.solver.find_path(word)
        if path:
            self._highlight_path_on_board(path)
            self.message_banner.config(text=f"Highlighting '{word.upper()}': {len(path)} letters", fg=THEME["accent_emerald"])

    def _highlight_path_on_board(self, path: List[Tuple[int, int]]):
        self.active_highlight = path
        self._update_tile_states()
        if self.highlight_after_id:
            self.root.after_cancel(self.highlight_after_id)
        self.highlight_after_id = self.root.after(4000, self._auto_clear_highlight)

    def _auto_clear_highlight(self):
        self.active_highlight.clear()
        self._update_tile_states()
        self.highlight_after_id = None

    def _show_round_summary(self):
        all_sols = self.solver.solve()
        RoundSummaryModal(
            parent=self.root,
            player_score=self.player_score,
            words_found=self.player_words,
            all_solutions=all_sols,
            on_play_again=self.start_new_game,
            on_inspect_solutions=self._set_solver_mode
        )

    # -------------------------------------------------------------
    # Dictionary & Settings
    # -------------------------------------------------------------
    def _init_dictionary(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        paths = [
            os.path.join(root_dir, "data", "dictionary.txt"),
            os.path.join(root_dir, "dictionary.txt"),
            os.path.join(os.path.dirname(__file__), "dictionary.txt")
        ]
        found = next((p for p in paths if os.path.exists(p)), None)
        if found:
            self._load_dictionary_from_file(found)
        else:
            self.dict_status_lbl.config(text="Dictionary not found. Click 'Dictionary' to load.", fg=THEME["accent_rose"])

    def _load_dictionary_from_file(self, filepath: str):
        def worker():
            try:
                t0 = time.time()
                trie = Trie.from_file(filepath)
                t1 = time.time()
                self.trie = trie
                self.solver.set_trie(trie)
                fname = os.path.basename(filepath)
                ms = (t1 - t0) * 1000
                self.root.after(0, lambda: self._on_dict_loaded(fname, trie.word_count, ms))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Dictionary Error", f"Failed to load: {e}"))

        self.dict_status_lbl.config(text="Indexing dictionary into Trie...", fg=THEME["accent_amber"])
        threading.Thread(target=worker, daemon=True).start()

    def _on_dict_loaded(self, fname: str, count: int, ms: float):
        self.dict_status_lbl.config(text=f"Dictionary: {fname} ({count:,} words indexed in {ms:.0f}ms)", fg=THEME["accent_emerald"])
        if self.game_mode == "SOLVER":
            self.solve_current_board()

    def _show_dictionary_menu(self):
        menu = tk.Menu(self.root, tearoff=0, bg=THEME["bg_card"], fg=THEME["text_primary"],
                       activebackground=THEME["accent_blue"], activeforeground="white")
        menu.add_command(label="📂 Load Custom Dictionary File (.txt)...", command=self._browse_dict)
        menu.add_command(label="🌐 Download Scrabble ENABLE1 List (172k+ words)", command=self._download_dict)
        menu.add_separator()
        menu.add_command(label="ℹ️ Dictionary Details", command=self._show_dict_info)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def _browse_dict(self):
        fp = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Dictionary", "*.dic"), ("All", "*.*")])
        if fp:
            self._load_dictionary_from_file(fp)

    def _download_dict(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        target = os.path.join(root_dir, "data", "enable_dictionary.txt")
        if messagebox.askyesno("Download Word List", "Download official Scrabble ENABLE1 dictionary (172,000+ words)?"):
            download_enable_dictionary(
                target_path=target,
                on_success=lambda p: self.root.after(0, lambda: self._load_dictionary_from_file(p)),
                on_error=lambda err: self.root.after(0, lambda: messagebox.showerror("Download Error", f"Error: {err}")),
                on_progress=lambda msg: self.root.after(0, lambda: self.dict_status_lbl.config(text=msg, fg=THEME["accent_amber"]))
            )

    def _show_dict_info(self):
        count = self.trie.word_count if self.trie else 0
        messagebox.showinfo("Dictionary Info", f"Total Indexed Words: {count:,}\nMinimum Length: 3 letters\nTrie Pruning Enabled")

    def _on_size_change(self, event=None):
        sel = self.size_var.get()
        self.grid_size = 3 if "3x3" in sel else (5 if "5x5" in sel else 4)
        self.start_new_game()

    def _on_timer_option_change(self, event=None):
        sel = self.timer_var.get()
        if "1 Min" in sel: self.time_limit = 60
        elif "2 Min" in sel: self.time_limit = 120
        elif "3 Min" in sel: self.time_limit = 180
        else: self.time_limit = 0
        self.start_new_game()

    def _toggle_sound(self):
        active = self.sound.toggle()
        self.sound_btn.config(text="🔊" if active else "🔇")

    def _enter_custom_grid(self):
        letters = ask_custom_grid(self.root, self.grid_size)
        if letters:
            self.board.set_custom(letters, self.grid_size)
            self.solver.cached_solutions.clear()
            self._render_board()
            self.clear_selection()
            if self.game_mode == "SOLVER":
                self.solve_current_board()
            else:
                self.message_banner.config(text="Custom grid loaded!", fg=THEME["accent_emerald"])


def main():
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = BoggleApp(root)
    root.mainloop()
