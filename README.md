# Word Master 🔠 (Freeform & Boggle Word Game)

A modern, high-performance word game and solver built with Python and Tkinter.

---

## 🌟 Key Features

1. **Select Letters in Any Order**:
   - Form meaningful English words using **any letters anywhere on the board**.
   - Letters do **not** need to be adjacent, horizontal, vertical, or diagonal!
   - Each tile on the board can be selected to spell words in any sequence.
2. **🔀 Rearrange Board**:
   - Click **🔀 Rearrange Board** at any time to shuffle the existing letters into new positions on the grid to spot words from a fresh perspective!
3. **Interactive Word Tray**:
   - As you click letters on the board, they appear in a visual **Word Tray** in the exact order selected.
   - Click any letter in the tray to remove it, or use <kbd>Backspace</kbd>.
4. **Dual Input (Mouse & Keyboard)**:
   - Click tiles on the board **OR** type directly on your keyboard. Matching letters from the board light up automatically!
5. **Instant Dictionary Validation**:
   - Validates words against **21,700+ curated English words** in `data/dictionary.txt`.
   - Ultra-fast Trie-pruned search verifies words in `< 0.3ms`.
6. **Rule Modes**:
   - **🔀 Any Letters / Any Order (Default)**: Freeform letter selection anywhere on the grid.
   - **🧭 Classic Boggle**: Strict adjacent neighbor rules (orthogonal & diagonal).
7. **Solver Mode**:
   - Instantly reveals all possible meaningful words that can be made from the board, grouped by word length.
   - Clicking any word in the list lights up its letters on the board!

---

## 🚀 How to Run

```bash
python main.py
```
*(or `python boggle_game.py`)*

To run all automated unit tests:
```bash
python -m unittest discover tests
```
