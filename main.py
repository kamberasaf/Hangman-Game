import randomword
import pygame
import math

# variables
MAX_NUM_OF_GUESSES = 6
current_state = 0
word = randomword.get_random_word().upper()
guessed_letters = []

# Setup Display
pygame.init()
WIDTH, HEIGHT = 780, 544
FPS = 60
clock = pygame.time.Clock()

# buttons
DISTANCE = 20
SEPERATE = 15
letters = []
START_X = round((WIDTH - (DISTANCE * 2 + SEPERATE) * 12 - 2 * DISTANCE) / 2)
START_Y = 470
A = 65
for i in range(26):
    X = START_X + DISTANCE + ((DISTANCE * 2 + SEPERATE) * (i % 13))
    Y = START_Y + ((i // 13) * (DISTANCE + SEPERATE * 2))
    letters.append([X, Y, chr(A + i), False])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
LETTERS_FONT = pygame.font.Font('arial_bold.ttf', 25)
GUESS_FONT = pygame.font.Font('arial_bold.ttf', 34)
WORD_FONT = pygame.font.Font('arial_bold.ttf', 40)
TITLE_FONT = pygame.font.Font('arial_bold.ttf', 60)


# Load Images
press_any_key = pygame.image.load("press any key.png")
hangman_title = pygame.image.load("Hangman title.png")

images = []
for i in range(7):
    image = pygame.image.load(f'hangman{i}.png')
    images.append(image)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


programIcon = pygame.image.load('loop-rope.png')
startBg = Background("game-background.jpg", [0, 0])
pygame.display.set_caption(" Hangman")
pygame.display.set_icon(programIcon)

# colors
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 102, 204)
DARK_BLUE = (0, 0, 153)
LIGHT_BROWN = (255, 204, 153)


def draw():
    screen.blit(startBg.image, startBg.rect)
    # current state
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    screen.blit(text, (20, 50))

    # draw buttons
    for letter in letters:
        x, y, ltr, clicked = letter
        if not clicked:
            pygame.draw.circle(screen, DARK_BLUE, (x, y), DISTANCE, 3)
            text = LETTERS_FONT.render(ltr, True, DARK_BLUE)
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # screen.blit(images[current_state], (280, 130))
    screen.blit(images[current_state], (280, 130))
    pygame.display.update()


def first_start():
    screen.blit(startBg.image, startBg.rect)
    screen.blit(hangman_title, (WIDTH / 2 - hangman_title.get_width() / 2, 15))
    pygame.display.update()
    pygame.time.delay(2000)
    screen.blit(press_any_key, (WIDTH / 2 - press_any_key.get_width() / 2, 415))
    pygame.display.update()


def new_game():
    global current_state
    global word
    global guessed_letters
    current_state = 0
    word = randomword.get_random_word().upper()
    guessed_letters = []
    for letter in letters:
        letter[3] = False


def finish_play():
    pygame.time.delay(1300)
    pygame.display.update()
    for event in pygame.event.get():
        pygame.time.delay(1700)
        try_again = LETTERS_FONT.render("Press any key to try again", True, BLACK)
        screen.blit(try_again, (WIDTH / 2 - try_again.get_width() / 2, 10))
        pygame.display.update()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            continue



def play():
    global current_state, guessed_letters
    pygame.display.update()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, clicked = letter
                    if not clicked:
                        dis = math.sqrt((m_x - x) ** 2 + (m_y - y) ** 2)
                        if dis < DISTANCE:
                            letter[3] = True
                            guessed_letters.append(letter[2])
                            if ltr not in word:
                                current_state += 1
                                break

        draw()
        won = True
        for letter in word:
            if letter not in guessed_letters:
                won = False
                break

        if won:
            text = TITLE_FONT.render("You won!", True, BLACK)
            screen.blit(text, (25, 120))
            finish_play()
            return

        if current_state == MAX_NUM_OF_GUESSES:
            text = TITLE_FONT.render("You lost!", True, BLACK)
            screen.blit(text, (25, 120))
            finish_play()
            return


if __name__ == '__main__':
    first_start()
    while True:
        for event in pygame.event.get():
            new_game()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.display.update()
                play()
