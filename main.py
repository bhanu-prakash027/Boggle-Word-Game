"""
Boggle Word Master - Main Application Entry Point.
Run this file to launch the game:
    python main.py
"""
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.boggle.ui.app import main

if __name__ == "__main__":
    main()

