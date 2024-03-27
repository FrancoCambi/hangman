import pygame, os, string, random

pygame.init()
pygame.font.init()


# WORDS
a, b = "ÁÉÍÓÚ", "AEIOU"
trans = str.maketrans(a, b)
with open("words.txt", "r", encoding="utf8") as fp:
    WORDS = [word.strip().upper().translate(trans) for word in fp if word != "\n" and " " not in word and len(word.strip()) <= 15]
fp.close()

# Screen const

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman!")
FPS = 60


# LOAD IMAGES AND FONTS

NUM_IMAGES = 7
images = []
for i in range(NUM_IMAGES):
    images.append(pygame.image.load(os.path.join('images', 'hangman' + str(i) + '.png')))

MAIN_FONT = pygame.font.SysFont('comicsans', 25)
WIN_FONT = pygame.font.SysFont('comicsnas', 200)
WORD_FONT = pygame.font.SysFont('comicsnas', 80)


# COLORS

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)  
BLACK = (0, 0, 0)

# USE CLASSES

class Game:
    HANG_POS = (53, 100)
    
    def __init__(self, letters_pos, letters):
        self.img = 0
        self.letters_pos = letters_pos
        self.letters = letters


# USE FUNC

def draw(win, game, rects, current_word, used_letter_list):
    used_circles = []
    win.fill(WHITE)
    win.blit(images[game.img], game.HANG_POS)
    for i in range(len(game.letters)):
        if game.letters[i] not in used_letter_list:
            letter = MAIN_FONT.render(game.letters[i], 1, BLACK)
            win.blit(letter, (game.letters_pos[i][0] - 12, game.letters_pos[i][1] - 18))
        else:
            used_circles.append(i)
    for i in range(len(game.letters_pos)):
        if i not in used_circles:
            x, y = game.letters_pos[i]
            pygame.draw.circle(win, BLACK, (x, y), 20, width=3)

    word = MAIN_FONT.render(current_word, 1, BLACK)
    x, y = game.HANG_POS
    win.blit(word, (x + images[game.img].get_width() + 100, y + images[game.img].get_height() / 2))
    

    pygame.display.update()

def clicked(game, rects, click):
    for i in range(len(rects)):
        if pygame.Rect.colliderect(click, rects[i]):
            return (game.letters[i])
    return ""

def fill_word(sel_word, letter_list):
    current_word = ""
    for i in range(len(sel_word)):
        if sel_word[i] in letter_list:
            for j in range(len(letter_list)):
                if sel_word[i] == letter_list[j] and current_word.count(letter_list[j]) < sel_word.count(letter_list[j]):
                    current_word += letter_list[j]
        else:
            current_word += " _ "
        
    return current_word

# MAIN FUNC

def main():

    clock = pygame.time.Clock()
    run = True

    letters_pos = [(60, 371)]
    letters = list(string.ascii_uppercase)
    rects = [pygame.Rect(40, 351, 40, 40)]
    for i in range(12):
        rects.append(pygame.Rect(letters_pos[i][0] + 35, 351, 40, 40))
        letters_pos.append((letters_pos[i][0] + 55, 371))
    letters_pos.append((60, 430))
    rects.append(pygame.Rect(40, 410, 40, 40))
    for i in range(12):
        rects.append(pygame.Rect(letters_pos[i][0] + 35, 410, 40, 40))
        letters_pos.append((letters_pos[i][0] + 55, 430))

    game = Game(letters_pos, letters)

    sel_word = random.choice(WORDS)
    sel_letter = ""
    letter_list = [] # letras corrects
    used_letter_list = [] # letras usadas

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            click = None
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                click = pygame.Rect(x, y, 1, 1)
                sel_letter = clicked(game, rects, click)
                if sel_letter in sel_word and sel_letter != "":
                    letter_list.append(sel_letter)
                    used_letter_list.append(sel_letter)
                elif sel_letter not in sel_word and sel_letter != "" and sel_letter not in used_letter_list:
                    used_letter_list.append(sel_letter)
                    game.img += 1
                    
        current_word = fill_word(sel_word, letter_list)
        
        draw(WIN, game, rects, current_word, used_letter_list)

        if current_word == sel_word:
            win_msg = WIN_FONT.render("You won!", 1, GREEN)
            word_was = WORD_FONT.render(f"Word: {sel_word}", 1, GREEN)
            WIN.blit(win_msg, (WIDTH / 2 - win_msg.get_width() / 2, HEIGHT / 2 - win_msg.get_height() / 2))
            WIN.blit(word_was, (WIDTH / 2 - word_was.get_width() / 2, HEIGHT / 2 + word_was.get_height()))
            pygame.display.update()
            pygame.time.wait(2000)
            run = False
            pygame.quit()
        
        if len(used_letter_list) >= NUM_IMAGES - 1:
            lost_msg = WIN_FONT.render(f"You lost!", 1, RED)
            word_was = WORD_FONT.render(f"Word: {sel_word}", 1, GREEN)
            WIN.blit(lost_msg, (WIDTH / 2 - lost_msg.get_width() / 2, HEIGHT / 2 - lost_msg.get_height() / 2))
            WIN.blit(word_was, (WIDTH / 2 - word_was.get_width() / 2, HEIGHT / 2 + word_was.get_height()))
            pygame.display.update()
            pygame.time.wait(1000)
            run = False
            pygame.quit()
            
if __name__ == "__main__":
    main()
