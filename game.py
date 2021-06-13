import pygame
from time import sleep
from numpy import random
from pygame.locals import *
import pygame_menu
import os
from functools import partial
snake_x = 0
snake_y = 0

pygame.init()

board = (800, 800)
dis = pygame.display.set_mode(board)
pygame.display.update()
pygame.display.set_caption('')
game_over = False

blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
orange = (255, 128, 0)
pink = (255, 153, 255)
dark_white = (145, 60, 255)
purple = (134, 61, 212)
aquamarine = (26, 135, 145)
light_blue = (80, 208, 255)
yellow = (255, 224, 32)
pale_pink = (255, 208, 160)
brown = (160, 128, 96)
gray = (128, 128, 128)
yellow_green = (96, 255, 128)
SNAKE_SIZE = 40


class SnakeLocation():
    def __init__(self, snake_x, snake_y):
        self.snake_x = snake_x
        self.snake_y = snake_y

    def __eq__(self, other):
        if self.snake_x == other[-1].snake_x and self.snake_y == other[-1].snake_y:
            return True
        return False


def playSound(name):
    fullname = os.path.join("dzwieki_gra",name)
    sound = pygame.mixer.Sound(fullname)
    return sound.play()
# pygame.sprite.Sprite
class Snake():
    def __init__(self, score):
        # super().__init__()
        self.snake = [SnakeLocation(snake_x, snake_y), SnakeLocation(snake_x + SNAKE_SIZE, snake_y),
                      SnakeLocation(snake_x + SNAKE_SIZE, snake_y)]
        self.direction = (SNAKE_SIZE, 0)
        self.life = 3
        self.score = score

    def __iter__(self):
        for x in self.snake:
            yield x

    def update_snake(self):
        # self.snake = self.snake[1:] + [SnakeLocation(self.snake[-1].snake_x+self.direction[0], self.snake[-1].snake_y+self.direction[1])]
        self.snake.pop(0)
        self.snake.append(
            SnakeLocation(self.snake[-1].snake_x + self.direction[0], self.snake[-1].snake_y + self.direction[1]))

    def draw_snake(self):
        for snake_single_location in self.snake[:-1]:
            pygame.draw.rect(dis, blue,
                             [snake_single_location.snake_x, snake_single_location.snake_y, SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.rect(dis, red, [self.snake[-1].snake_x, self.snake[-1].snake_y, SNAKE_SIZE, SNAKE_SIZE])

    def draw_life(self):
        vector = 0
        heart_size = (50, 50)
        for number_of_life in range(self.life):
            img = pygame.image.load('heart.png').convert_alpha()
            re = pygame.Rect((0 + vector, 0), (30 + vector, 30))
            img = pygame.transform.scale(img, heart_size)
            colorkey = img.get_at((5, 5))
            img.set_colorkey(colorkey, RLEACCEL)
            dis.blit(img, re)
            vector += 20


    def find_colision(self, apple, score):
        if apple.apple.apple_x == self.snake[-1].snake_x and apple.apple.apple_y == self.snake[-1].snake_y:
            apple.random_apple()
            self.snake.append(SnakeLocation(self.snake[-1].snake_x, self.snake[-1].snake_y))
            score.add_points()
            sound_list = ['alez_on_zre_koperek.mp3', 'czegos_takiego_nigdy_nie_jadłem.mp3', 'czuc_aromat_drewna.mp3',
                          'jest_po_prostu_idealne.mp3', 'mamy_pozostawac_na_czczo.mp3', 'o_Jezu_ale_to_dobre.mp3']
            name = sound_list[random.randint(0, 6)]
            fullname = os.path.join("dzwieki_gra", name)
            sound = pygame.mixer.Sound(fullname)
            sound.play()

    def check_colision_with_board(self):

        if self.snake[-1].snake_x >= board[0] or self.snake[-1].snake_x < 0 or self.snake[-1].snake_y >= board[1] or \
                self.snake[-1].snake_y < 0:
            if self.life == 1:
                pygame.time.wait(1050)  # _> go to menu after some time
                with open('leaderboard.txt', 'a') as file:
                    file.write(f"{self.score.gracz} {self.score.score}\n")
                mainMenu()
            self.life -= 1
            pygame.time.wait(1050)
            self.snake = [SnakeLocation(snake_x, snake_y), SnakeLocation(snake_x + SNAKE_SIZE, snake_y),
                          SnakeLocation(snake_x + SNAKE_SIZE, snake_y)]
            self.direction = (SNAKE_SIZE, 0)
            playSound('dubdubdubdubdub.mp3')


    def check_colision_with_self(self):
        for snake_single_location in self.snake[:-1]:
            if snake_single_location == self.snake:
                if self.life == 1:
                    pygame.time.wait(1050)  # _> go to menu after some time
                    with open('leaderboard.txt', 'a') as file:
                        file.write(f"{self.score.name} {self.score.score}")
                    mainMenu()
                self.life -= 1
                pygame.time.wait(1050)
                self.snake = [SnakeLocation(snake_x, snake_y), SnakeLocation(snake_x + SNAKE_SIZE, snake_y),
                              SnakeLocation(snake_x + SNAKE_SIZE, snake_y)]
                self.direction = (SNAKE_SIZE, 0)
                playSound('bububububibibi.mp3')



class AppleLocation():
    def __init__(self, snake):
        self.random(snake)

    def random(self, snake):

        self.apple_x = random.randint(1, board[0]) // SNAKE_SIZE * SNAKE_SIZE
        self.apple_y = random.randint(1, board[1]) // SNAKE_SIZE * SNAKE_SIZE
        while self.apple_x in [obj.snake_x for obj in snake.snake]:
            self.apple_x = random.randint(1, board[0] - 2) // SNAKE_SIZE * SNAKE_SIZE
        while self.apple_y in [obj.snake_y for obj in snake.snake]:
            self.apple_y = random.randint(1, board[0] - 2) // SNAKE_SIZE * SNAKE_SIZE



class Apple():
    def __init__(self, snake):
        self.snake = snake
        self.apple = AppleLocation(snake)

    def draw(self):
        img = pygame.image.load('apple5.png').convert_alpha()
        re = pygame.Rect((self.apple.apple_x, self.apple.apple_y),
                         (self.apple.apple_x + SNAKE_SIZE, self.apple.apple_y + SNAKE_SIZE))
        img = pygame.transform.scale(img, (SNAKE_SIZE, SNAKE_SIZE))
        colorkey = img.get_at((0, 0))  # odczytaj kolor w punkcie (0,0)
        img.set_colorkey(colorkey, RLEACCEL)  # ustaw kolor jako przezroczysty
        dis.blit(img, re)

    def random_apple(self):
        self.apple = AppleLocation(self.snake)


class Score():
    def __init__(self):
        self.gracz = 'player1'
        self.score = 0

    def add_points(self):
        self.score += 10

    def draw_score(self):
        font = pygame.font.SysFont(None, 50)
        img = font.render(str(self.score), True, blue)
        dis.blit(img, (board[0] - 20 * len(str(self.score)), 0))



class Game():
    def __init__(self):
        self.score = Score()
        self.snake = Snake(self.score)
        self.clock = pygame.time.Clock()
        self.apple = Apple(self.snake)
        self.apple2 = Apple(self.snake)
        self.apple3 = Apple(self.snake)
        self.apple4 = Apple(self.snake)
        self.apple5 = Apple(self.snake)
        self.apple6 = Apple(self.snake)
        self.time_wait, self.clock_tick = 40, 30
        self.level = 1

    def setdifficulty(self, _, level):
        self.level = level
        if level == 1:
            self.time_wait, self.clock_tick = 40, 30
        if level == 2:
            self.time_wait, self.clock_tick = 1, 60
        if level == 3:
            self.time_wait, self.clock_tick = 1, 60

    def draw_background(self):
        if self.level == 3:
            img = pygame.image.load('illusion8.jpg')
        else:
            img = pygame.image.load('snake_background2.jpg')
        re = pygame.Rect((0, 0), board)
        img = pygame.transform.scale(img, board)
        img = img.convert()
        dis.blit(img, re)

    def set_score(self, *args):
        score, game, gracz = args
        score.gracz = gracz
        game.snake.score.gracz = gracz
        game.score = score
        game.snake.score.score = score.score

    def run_game(self):
        while not game_over:
            index = 0
            for event in pygame.event.get():
                # obsługa zdarzeń
                # warunki do zmiany pozycji obiektu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction != (SNAKE_SIZE, 0):
                            self.snake.direction = (- 1 * SNAKE_SIZE, 0)
                            break
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction != (- 1 * SNAKE_SIZE, 0):
                            self.snake.direction = (SNAKE_SIZE, 0)
                            break
                    if event.key == pygame.K_UP:
                        if self.snake.direction != (0, SNAKE_SIZE):
                            self.snake.direction = (0, - 1 * SNAKE_SIZE)
                            break
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction != (0, - 1 * SNAKE_SIZE):
                            self.snake.direction = (0, SNAKE_SIZE)
                            break
            self.snake.update_snake()
            self.snake.check_colision_with_self()
            self.snake.check_colision_with_board()
            self.draw_background()
            self.snake.draw_life()
            self.snake.score.draw_score()
            self.snake.draw_snake()
            self.apple.draw()
            self.apple2.draw()
            self.apple3.draw()
            self.apple4.draw()
            self.apple5.draw()
            self.apple6.draw()
            self.snake.find_colision(self.apple, self.snake.score)
            self.snake.find_colision(self.apple2, self.snake.score)
            self.snake.find_colision(self.apple3, self.snake.score)
            self.snake.find_colision(self.apple4, self.snake.score)
            self.snake.find_colision(self.apple5, self.snake.score)
            self.snake.find_colision(self.apple6, self.snake.score)
            pygame.display.update()
            pygame.time.wait(self.time_wait)
            self.clock.tick(self.clock_tick)


font = pygame_menu.font.FONT_NEVIS

myimage = pygame_menu.baseimage.BaseImage(
    image_path=("backgr.jpg"),
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)

mytheme = pygame_menu.themes.THEME_SOLARIZED.copy()
mytheme.widget_font = font
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
mytheme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
mytheme.background_color = myimage



def mainMenu():
    game = Game()
    score = Score()
    action = partial(game.set_score, score, game)
    menu = pygame_menu.Menu("Main Menu", board[0], board[1], theme=mytheme)
    menu.add.text_input('Nick:', 'player1', maxchar=9, onchange=action)
    menu.add.button('Play', game.run_game)
    menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2), ('Illusion', 3)], onchange=game.setdifficulty)
    menu.add.button('How to play', how_to_play)
    menu.add.button('Autors', autors)
    menu.add.button('Scoreboard ', scoreboard)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(dis)



class Scoreboard():
    def __init__(self):
        self.data = [] #[(name, score), ]

    def read_data(self):
        with open('leaderboard.txt', 'r') as file:
            for linie in file.readlines():
                self.data.append(linie[:-1].split(' '))

    def sort_data(self):
        self.data = sorted(self.data, key=lambda x: int(x[1]), reverse=True)

def scoreboard():
    score = Scoreboard()
    score.read_data()
    score.sort_data()
    menu = pygame_menu.Menu('Scoreboard', board[0], board[1], theme=mytheme)
    menu.add.label("TOP 10 SCORE", font_size=30)
    for tupla in score.data[:10]:
        menu.add.label(f"{tupla[0]} Score:{tupla[1]}", font_size=30)
    menu.add.button('Back', mainMenu)
    menu.mainloop(dis)


def how_to_play():
    menu = pygame_menu.Menu('How to play', board[0], board[1], theme=mytheme)
    description = 'Enter your nickname \n Choose level of difficulty\n Don\'t hit yourself or game edge\n' \
                  'Collect apples increasing  your score \n You can check your score after game'

    menu.add.label(description, font_size=30)
    menu.add.button('Back', mainMenu)
    menu.mainloop(dis)


def autors():
    menu = pygame_menu.Menu('Autors', board[0], board[1], theme=mytheme)
    description = 'Roch Kalemba \n Matematyka stosowana 1 rok\n Programowanie'
    menu.add.label(description, font_size=30)
    menu.add.button('Back', mainMenu)
    menu.mainloop(dis)

mainMenu()

