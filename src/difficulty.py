"""
This module adds a game difficulty selector to the Hangman game.
"""
import pygame

class DifficultySelector:
    """
    A class to handle difficulty selection for the Hangman game.
    
    This class creates a screen where players can choose a game difficulty
    and optionally a word category before starting the game.
    """
    
    def __init__(self, screen, background, font_path):
        """
        Initialize the difficulty selector.
        
        Args:
            screen: The pygame surface to draw on
            background: The background sprite
            font_path: Path to the font file
        """
        self.screen = screen
        self.background = background
        
        # Fonts
        self.title_font = pygame.font.Font(font_path, 50)
        self.option_font = pygame.font.Font(font_path, 30)
        self.info_font = pygame.font.Font(font_path, 20)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARK_BLUE = (0, 0, 153)
        self.LIGHT_BLUE = (0, 102, 204)
        self.GREEN = (0, 153, 0)
        self.RED = (204, 0, 0)
        self.YELLOW = (204, 204, 0)
        
        # Difficulty options
        self.difficulties = [
            {"name": "Easy", "color": self.GREEN, "desc": "3-5 letter words"},
            {"name": "Medium", "color": self.YELLOW, "desc": "6-7 letter words"},
            {"name": "Hard", "color": self.RED, "desc": "8+ letter words, uncommon letters"}
        ]
        
        # Category information
        from src.randomword import get_word_categories
        self.categories = get_word_categories()
        self.category_names = list(self.categories.keys())
        self.selected_category = None
        
        # Button dimensions and positions
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.button_width = 200
        self.button_height = 60
        self.button_margin = 30
        
        # Calculate positions for difficulty buttons
        self.diff_buttons = []
        start_y = 180
        for i, diff in enumerate(self.difficulties):
            btn_x = (self.WIDTH - self.button_width) // 2
            btn_y = start_y + i * (self.button_height + self.button_margin)
            
            self.diff_buttons.append({
                "rect": pygame.Rect(btn_x, btn_y, self.button_width, self.button_height),
                "difficulty": diff["name"].lower(),
                "name": diff["name"],
                "color": diff["color"],
                "desc": diff["desc"]
            })
        
        # Calculate positions for category buttons if there are any
        self.cat_buttons = []
        if self.categories:
            # Position category buttons on the right side
            cat_start_x = self.WIDTH - 250
            cat_start_y = 180
            cat_button_width = 180
            cat_button_height = 40
            
            for i, cat in enumerate(self.category_names):
                # Only show the first 8 categories to avoid overcrowding
                if i >= 8:
                    break
                    
                btn_x = cat_start_x
                btn_y = cat_start_y + i * (cat_button_height + 15)
                
                self.cat_buttons.append({
                    "rect": pygame.Rect(btn_x, btn_y, cat_button_width, cat_button_height),
                    "name": cat,
                    "selected": False
                })
    
    def draw(self):
        """
        Draw the difficulty selection screen.
        """
        # Draw background
        self.screen.blit(self.background.image, self.background.rect)
        
        # Draw title
        title = self.title_font.render("Select Difficulty", True, self.BLACK)
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 50))
        
        # Draw difficulty buttons
        for btn in self.diff_buttons:
            pygame.draw.rect(self.screen, btn["color"], btn["rect"], border_radius=10)
            pygame.draw.rect(self.screen, self.BLACK, btn["rect"], 3, border_radius=10)
            
            # Button text
            text = self.option_font.render(btn["name"], True, self.BLACK)
            text_x = btn["rect"].centerx - text.get_width()//2
            text_y = btn["rect"].centery - text.get_height()//2
            self.screen.blit(text, (text_x, text_y))
            
            # Description text
            desc = self.info_font.render(btn["desc"], True, self.BLACK)
            desc_x = btn["rect"].centerx - desc.get_width()//2
            desc_y = btn["rect"].bottom + 5
            self.screen.blit(desc, (desc_x, desc_y))
        
        # Draw category title if there are categories
        if self.categories:
            cat_title = self.option_font.render("Optional: Choose Category", True, self.BLACK)
            self.screen.blit(cat_title, (self.WIDTH - 250 - cat_title.get_width()//2, 130))
            
            # Draw category buttons
            for btn in self.cat_buttons:
                # Use a different color for selected category
                color = self.LIGHT_BLUE if btn["selected"] else self.WHITE
                pygame.draw.rect(self.screen, color, btn["rect"], border_radius=5)
                pygame.draw.rect(self.screen, self.BLACK, btn["rect"], 2, border_radius=5)
                
                # Button text
                text = self.info_font.render(btn["name"].capitalize(), True, self.BLACK)
                text_x = btn["rect"].centerx - text.get_width()//2
                text_y = btn["rect"].centery - text.get_height()//2
                self.screen.blit(text, (text_x, text_y))
        
        # Draw start button at the bottom
        start_btn = pygame.Rect((self.WIDTH - 250)//2, self.HEIGHT - 100, 250, 60)
        pygame.draw.rect(self.screen, self.DARK_BLUE, start_btn, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, start_btn, 3, border_radius=10)
        
        start_text = self.option_font.render("Start Game", True, self.WHITE)
        start_x = start_btn.centerx - start_text.get_width()//2
        start_y = start_btn.centery - start_text.get_height()//2
        self.screen.blit(start_text, (start_x, start_y))
        
        pygame.display.update()
        
        return start_btn
    
    def handle_click(self, pos):
        """
        Handle mouse clicks on the difficulty selection screen.
        
        Args:
            pos: The (x, y) position of the mouse click
            
        Returns:
            tuple: (difficulty, category) if Start Game is clicked, None otherwise
        """
        # Check difficulty button clicks
        for btn in self.diff_buttons:
            if btn["rect"].collidepoint(pos):
                # Set this as the selected difficulty
                for b in self.diff_buttons:
                    b["color"] = self.GREEN if b["name"] == "Easy" else \
                               self.YELLOW if b["name"] == "Medium" else \
                               self.RED
                
                # Highlight the selected button
                btn["color"] = (btn["color"][0] + 50, btn["color"][1] + 50, btn["color"][2] + 50)
                return None
        
        # Check category button clicks
        for btn in self.cat_buttons:
            if btn["rect"].collidepoint(pos):
                # Toggle selection
                btn["selected"] = not btn["selected"]
                
                # Deselect other category buttons
                if btn["selected"]:
                    self.selected_category = btn["name"]
                    for other_btn in self.cat_buttons:
                        if other_btn != btn:
                            other_btn["selected"] = False
                else:
                    self.selected_category = None
                
                return None
        
        # Check if Start Game button is clicked
        start_btn = pygame.Rect((self.WIDTH - 250)//2, self.HEIGHT - 100, 250, 60)
        if start_btn.collidepoint(pos):
            # Find selected difficulty
            difficulty = "medium"  # Default
            for btn in self.diff_buttons:
                if btn["color"] != (self.GREEN if btn["name"] == "Easy" else \
                                  self.YELLOW if btn["name"] == "Medium" else \
                                  self.RED):
                    difficulty = btn["difficulty"]
                    break
            
            return (difficulty, self.selected_category)
        
        return None
    
    def run(self):
        """
        Run the difficulty selector screen.
        
        Returns:
            tuple: (difficulty, category) selections
        """
        running = True
        start_btn = self.draw()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result:
                        return result
                    
                    # Redraw after handling click
                    start_btn = self.draw()
            
            pygame.display.update()
        
        return None