"""
Main entry point for the Hangman game.
"""
import pygame
from src.game import HangmanGame

def main():
    """
    Initialize and run the Hangman game.
    """
    pygame.init()
    game = HangmanGame()
    game.run()

if __name__ == "__main__":
    main()