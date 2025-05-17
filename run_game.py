"""
Launcher script for the educational environmental game.
This script ensures proper path resolution for assets and documentation files.
"""
import os
import sys
import pygame

# Ensure we're running from the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add src directory to the Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Add assets path as an environment variable for easier access in game files
os.environ['ASSETS_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.environ['DOCS_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')

# Initialize pygame
pygame.init()

# Import the main menu to start the game
from main_menu import main_menu

if __name__ == "__main__":
    print("Starting Environmental Education Game...")
    print(f"Assets path: {os.environ['ASSETS_PATH']}")
    print(f"Source path: {src_path}")
    main_menu()
