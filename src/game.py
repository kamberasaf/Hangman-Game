import math
import pygame
from src.randomword import get_random_word, get_random_word_from_category
from src.difficulty import DifficultySelector

class HangmanGame:
    """
    Main game class for Hangman.
    """
    # Game constants
    WIDTH, HEIGHT = 780, 544
    FPS = 60
    MAX_NUM_OF_GUESSES = 6
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (0, 102, 204)
    DARK_BLUE = (0, 0, 153)
    LIGHT_BROWN = (255, 204, 153)
    
    def __init__(self):
        """
        Initialize the game, setup display, fonts, and load assets.
        """
        # Game state
        self.current_state = 0
        self.word = ""
        self.difficulty = "medium"
        self.category = None
        self.guessed_letters = []
        self.running = True
        
        # Setup pygame
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.LETTERS_FONT = pygame.font.Font('assets/fonts/arial_bold.ttf', 25)
        self.GUESS_FONT = pygame.font.Font('assets/fonts/arial_bold.ttf', 34)
        self.WORD_FONT = pygame.font.Font('assets/fonts/arial_bold.ttf', 40)
        self.TITLE_FONT = pygame.font.Font('assets/fonts/arial_bold.ttf', 60)
        
        # Create letter buttons
        self.setup_buttons()
        
        # Load images
        self.press_any_key = pygame.image.load("assets/images/press_any_key.png")
        self.hangman_title = pygame.image.load("assets/images/hangman_title.png")
        
        self.images = []
        for i in range(7):
            image = pygame.image.load(f'assets/images/hangman{i}.png')
            self.images.append(image)
        
        # Load background and icon
        self.background = self.load_background("assets/images/game_background.jpg", [0, 0])
        
        # Set window properties
        program_icon = pygame.image.load('assets/images/loop_rope.png')
        pygame.display.set_caption("Hangman")
        pygame.display.set_icon(program_icon)
        
        # Create difficulty selector
        self.difficulty_selector = DifficultySelector(
            self.screen, 
            self.background, 
            'assets/fonts/arial_bold.ttf'
        )
    
    def setup_buttons(self):
        """
        Setup the letter buttons for the game.
        """
        self.letters = []
        DISTANCE = 20
        SEPERATE = 15
        START_X = round((self.WIDTH - (DISTANCE * 2 + SEPERATE) * 12 - 2 * DISTANCE) / 2)
        START_Y = 470
        A = 65
        
        for i in range(26):
            X = START_X + DISTANCE + ((DISTANCE * 2 + SEPERATE) * (i % 13))
            Y = START_Y + ((i // 13) * (DISTANCE + SEPERATE * 2))
            self.letters.append([X, Y, chr(A + i), False])
    
    def load_background(self, image_file, location):
        """
        Load the background image as a sprite.
        
        Args:
            image_file: Path to the background image
            location: [x, y] position to place the background
            
        Returns:
            A pygame.sprite.Sprite object with the background
        """
        class Background(pygame.sprite.Sprite):
            def __init__(self, image_file, location):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(image_file)
                self.rect = self.image.get_rect()
                self.rect.left, self.rect.top = location
        
        return Background(image_file, location)
    
    def draw(self):
        """
        Draw the game state to the screen.
        """
        # Draw background
        self.screen.blit(self.background.image, self.background.rect)
        
        # Draw word with placeholders for unguessed letters
        display_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        
        text = self.WORD_FONT.render(display_word, True, self.BLACK)
        self.screen.blit(text, (20, 50))
        
        # Draw difficulty and category info if available
        difficulty_text = self.LETTERS_FONT.render(
            f"Difficulty: {self.difficulty.capitalize()}", True, self.BLACK
        )
        self.screen.blit(difficulty_text, (self.WIDTH - difficulty_text.get_width() - 20, 20))
        
        if self.category:
            category_text = self.LETTERS_FONT.render(
                f"Category: {self.category.capitalize()}", True, self.BLACK
            )
            self.screen.blit(category_text, (self.WIDTH - category_text.get_width() - 20, 50))
        
        # Draw letter buttons
        for letter in self.letters:
            x, y, ltr, clicked = letter
            if not clicked:
                pygame.draw.circle(self.screen, self.DARK_BLUE, (x, y), 20, 3)
                text = self.LETTERS_FONT.render(ltr, True, self.DARK_BLUE)
                self.screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
        
        # Draw hangman
        self.screen.blit(self.images[self.current_state], (280, 130))
        
        pygame.display.update()
    
    def show_start_screen(self):
        """
        Show the game's start screen.
        """
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.hangman_title, (self.WIDTH / 2 - self.hangman_title.get_width() / 2, 15))
        pygame.display.update()
        pygame.time.delay(2000)
        
        self.screen.blit(self.press_any_key, (self.WIDTH / 2 - self.press_any_key.get_width() / 2, 415))
        pygame.display.update()
        
        # Wait for key or mouse press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        return True
    
    def select_difficulty(self):
        """
        Show the difficulty selection screen.
        
        Returns:
            bool: True if selection was made, False if user quit
        """
        result = self.difficulty_selector.run()
        if result:
            self.difficulty, self.category = result
            return True
        return False
    
    def reset_game(self):
        """
        Reset the game state for a new game.
        """
        self.current_state = 0
        
        # Get a new word based on difficulty and category
        if self.category:
            self.word = get_random_word_from_category(self.category).upper()
        else:
            self.word = get_random_word(self.difficulty).upper()
            
        self.guessed_letters = []
        
        # Reset letter buttons
        for letter in self.letters:
            letter[3] = False
    
    def check_game_over(self):
        """
        Check if the game is won or lost.
        
        Returns:
            int: 1 if game is won, -1 if game is lost, 0 if game continues
        """
        # Check if player won
        won = True
        for letter in self.word:
            if letter not in self.guessed_letters:
                won = False
                break
        
        if won:
            return 1
        
        # Check if player lost
        if self.current_state == self.MAX_NUM_OF_GUESSES:
            return -1
        
        # Game continues
        return 0
    
    def show_game_over(self, result):
        """
        Show game over screen with win/lose message.
        
        Args:
            result: 1 for win, -1 for lose
        """
        if result == 1:
            text = self.TITLE_FONT.render("You won!", True, self.BLACK)
        else:
            text = self.TITLE_FONT.render("You lost!", True, self.BLACK)
            # Show the correct word
            word_text = self.LETTERS_FONT.render(f"The word was: {self.word}", True, self.BLACK)
            self.screen.blit(word_text, (self.WIDTH / 2 - word_text.get_width() / 2, 250))
        
        self.screen.blit(text, (25, 120))
        
        # Show try again message
        pygame.time.delay(1300)
        try_again = self.LETTERS_FONT.render("Press any key to try again", True, self.BLACK)
        self.screen.blit(try_again, (self.WIDTH / 2 - try_again.get_width() / 2, 10))
        pygame.display.update()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        return True
    
    def play_round(self):
        """
        Play one round of the game.
        
        Returns:
            bool: True if game should continue, False if user quit
        """
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()
            
            # Draw current state
            self.draw()
            
            # Check game over condition
            result = self.check_game_over()
            if result != 0:
                self.running = False
                if not self.show_game_over(result):
                    return False
        
        return True
    
    def handle_mouse_click(self):
        """
        Handle mouse click events for letter selection.
        """
        m_x, m_y = pygame.mouse.get_pos()
        
        for letter in self.letters:
            x, y, ltr, clicked = letter
            if not clicked:
                dis = math.sqrt((m_x - x) ** 2 + (m_y - y) ** 2)
                if dis < 20:  # DISTANCE
                    letter[3] = True
                    self.guessed_letters.append(ltr)
                    
                    # Increment state if wrong guess
                    if ltr not in self.word:
                        self.current_state += 1
                    break
    
    def run(self):
        """
        Main game loop.
        """
        # Show start screen
        if not self.show_start_screen():
            return
        
        # Main game loop
        while True:
            # Show difficulty selection
            if not self.select_difficulty():
                return
            
            # Initialize the game with selected settings
            self.reset_game()
            
            # Play the game
            if not self.play_round():
                break