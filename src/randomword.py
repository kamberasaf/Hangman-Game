"""
Module for generating random words for the Hangman game.
"""
import random
import os

def load_words_from_file(filename):
    """
    Load words from a text file.
    
    Args:
        filename: Path to the word list file
        
    Returns:
        list: List of words loaded from the file
    """
    try:
        with open(filename, 'r') as file:
            # Strip whitespace and filter out empty lines and words with non-alphabetic characters
            words = [word.strip().lower() for word in file.readlines()]
            return [word for word in words if word and word.isalpha() and len(word) >= 3]
    except FileNotFoundError:
        print(f"Warning: Word list file '{filename}' not found. Using fallback word list.")
        return get_fallback_words()

def get_fallback_words():
    """
    Provides a fallback list of words if the external file is not available.
    
    Returns:
        list: A list of words
    """
    return [
        "python", "hangman", "programming", "computer", "algorithm",
        "keyboard", "function", "variable", "pygame", "dictionary",
        "developer", "challenge", "solution", "interface", "module",
        "software", "hardware", "network", "database", "graphics",
        "internet", "browser", "website", "application", "security",
        "gaming", "virtual", "digital", "memory", "processor",
        "monitor", "keyboard", "speaker", "webcam", "microphone",
        "server", "client", "language", "framework", "library"
    ]

def get_words_by_difficulty(difficulty='medium'):
    """
    Get words filtered by difficulty level.
    
    Args:
        difficulty: 'easy', 'medium', or 'hard'
        
    Returns:
        list: Words of appropriate difficulty
    """
    all_words = get_all_words()
    
    if difficulty == 'easy':
        # Easy: 3-5 letter words
        return [word for word in all_words if 3 <= len(word) <= 5]
    elif difficulty == 'hard':
        # Hard: 8+ letter words or words with uncommon letters (j, q, x, z)
        return [word for word in all_words if len(word) >= 8 or 
                any(letter in word for letter in 'jqxz')]
    else:
        # Medium: 6-7 letter words not containing uncommon letters
        return [word for word in all_words if 6 <= len(word) <= 7 and 
                not any(letter in word for letter in 'jqxz')]

def get_all_words():
    """
    Get all available words.
    
    Returns:
        list: Complete list of words
    """
    # First try to load words from external files
    words_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'wordlists')
    
    # Try multiple possible word list files
    potential_files = [
        os.path.join(words_dir, 'wordlist.txt'),
        os.path.join(words_dir, 'words.txt'),
        '/usr/share/dict/words'  # Common location on Unix-like systems
    ]
    
    for file_path in potential_files:
        if os.path.exists(file_path):
            return load_words_from_file(file_path)
    
    # If no files are found, use the fallback list
    return get_fallback_words()

def get_random_word(difficulty=None):
    """
    Returns a random word for the Hangman game.
    
    Args:
        difficulty: Optional difficulty level ('easy', 'medium', 'hard')
        
    Returns:
        str: A random word
    """
    if difficulty:
        word_list = get_words_by_difficulty(difficulty)
    else:
        word_list = get_all_words()
    
    return random.choice(word_list)

def get_word_categories():
    """
    Returns available word categories if categorized word lists exist.
    
    Returns:
        dict: A dictionary of category names to word lists
    """
    categories = {}
    categories_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 'assets', 'wordlists', 'categories')
    
    # If the categories directory exists, load each file as a category
    if os.path.exists(categories_dir):
        for filename in os.listdir(categories_dir):
            if filename.endswith('.txt'):
                category_name = filename[:-4]  # Remove .txt extension
                file_path = os.path.join(categories_dir, filename)
                categories[category_name] = load_words_from_file(file_path)
    
    return categories

def get_random_word_from_category(category):
    """
    Get a random word from a specific category.
    
    Args:
        category: The name of the category
        
    Returns:
        str: A random word from the category, or None if category doesn't exist
    """
    categories = get_word_categories()
    
    if category in categories and categories[category]:
        return random.choice(categories[category])
    
    # Fallback to regular random word if category doesn't exist
    return get_random_word()