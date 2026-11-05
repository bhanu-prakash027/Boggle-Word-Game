"""
Backward compatibility launcher for Boggle Word Master.
You can also run directly with: python main.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.boggle.ui.app import main

if __name__ == "__main__":
    main()
