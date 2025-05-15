# Advanced Hangman Game

![Hangman Game Screenshot](assets/images/screenshot.png)

A classic Hangman game with multiple difficulty levels and word categories, built with Python and Pygame.

## Features

- Interactive GUI with Pygame
- Multiple difficulty levels (Easy, Medium, Hard)
- Categorized word lists (Animals, Countries, Foods, and more)
- Extensive word database
- Animated hangman progression
- Win/lose detection
- Play again functionality

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kamberasaf/Hangman-Game.git
cd Hangman-Game
```

2. Install the required dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python main.py
```

## How to Play

1. Start the game by pressing any key at the title screen
2. Select a difficulty level:
   - **Easy**: 3-5 letter words
   - **Medium**: 6-7 letter words
   - **Hard**: 8+ letter words or words with uncommon letters
3. Optionally select a word category (Animals, Countries, Foods, etc.)
4. Guess letters by clicking on them with your mouse
5. If your guess is correct, the letter will appear in the word
6. If your guess is wrong, more of the hangman will be drawn
7. Win by guessing all letters in the word before the hangman is complete
8. After a game ends, press any key to play again

## Game Controls

- **Mouse Click**: Select a letter or button
- **Any Key**: Continue at title and game over screens

## Development

This game was developed as an introduction to the Pygame library, focusing on:
- Object-Oriented Programming
- Event-driven programming
- Game state management
- UI/UX design

## Project Structure

```
Hangman-Game/
├── assets/               # Game assets 
│   ├── fonts/            # Font files
│   ├── images/           # Image files
│   └── wordlists/        # Word lists by category
│       └── categories/   # Categorized word lists
├── src/                  # Source code
│   ├── difficulty.py     # Difficulty selector
│   ├── game.py           # Main game logic
│   └── randomword.py     # Word generation
├── .gitignore            # Git ignore file
├── LICENSE               # License information  
├── README.md             # This file
└── main.py               # Entry point
```

## Extending the Game

### Adding New Word Categories

1. Create a new text file in `assets/wordlists/categories/`
2. Add one word per line (lowercase, no special characters)
3. The category will be automatically detected by the game

### Customizing Difficulty Levels

You can adjust the difficulty criteria in `src/randomword.py`:
- **Easy**: Words with 3-5 letters
- **Medium**: Words with 6-7 letters
- **Hard**: Words with 8+ letters or containing uncommon letters (j, q, x, z)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by Asaf Kamber

## Acknowledgments

- Pygame community for the excellent documentation
- [OpenGameArt](https://opengameart.org/) for inspiration on game assets