import pygame
from time import sleep
from numpy import random

snake_x = 0
snake_y = 0

pygame.init()
board = (150, 150)
dis = pygame.display.set_mode(board)
pygame.display.update()
pygame.display.set_caption('')
game_over = False
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)


class SnakeLocation():
    def __init__(self, snake_x, snake_y):
        self.snake_x = snake_x
        self.snake_y = snake_y

    def __eq__(self, other):
        if self.snake_x == other[-1].snake_x and self.snake_y == other[-1].snake_y:
            return True
        return False


# pygame.sprite.Sprite
class Snake():
    def __init__(self, rozmiar=3):
        # super().__init__()
        self.snake = [SnakeLocation(snake_x, snake_y), SnakeLocation(snake_x + 10, snake_y),
                      SnakeLocation(snake_x + 20, snake_y)]
        self.direction = (10, 0)

    def update_snake(self):
        # self.snake = self.snake[1:] + [SnakeLocation(self.snake[-1].snake_x+self.direction[0], self.snake[-1].snake_y+self.direction[1])]
        self.snake.pop(0)
        self.snake.append(
            SnakeLocation(self.snake[-1].snake_x + self.direction[0], self.snake[-1].snake_y + self.direction[1]))

    def draw_snake(self):
        for snake_single_location in self.snake[:-1]:
            pygame.draw.rect(dis, blue, [snake_single_location.snake_x, snake_single_location.snake_y, 10, 10])
        pygame.draw.rect(dis, red, [self.snake[-1].snake_x, self.snake[-1].snake_y, 10, 10])

    def find_colision(self, apple, score):
        if apple.apple.apple_x == self.snake[-1].snake_x and apple.apple.apple_y == self.snake[-1].snake_y:
            apple.random_apple()
            self.snake.append(SnakeLocation(self.snake[-1].snake_x, self.snake[-1].snake_y))
            score.add_points()

    def check_colision_with_board(self):
        print(f'{self.snake[-1].snake_x} snake_x,  {board[0]} boread x')
        if self.snake[-1].snake_x >= board[0] or self.snake[-1].snake_x < 0 or self.snake[-1].snake_y >= board[1] or \
                self.snake[-1].snake_y < 0:
            pygame.time.wait(2350)  # _> go to menu after some time
            pygame.quit()
            quit()

    def check_colision_with_self(self):
        for snake_single_location in self.snake[:-1]:
            if snake_single_location != self.snake:
                continue
            else:
                pygame.quit()
                quit()


class AppleLocation():
    def __init__(self, snake):
        self.random(snake)

    def random(self, snake):

        self.apple_x = random.randint(1, board[0]) // 10 * 10
        self.apple_y = random.randint(1, board[1]) // 10 * 10
        while True:
            for snake_single_location in snake.snake:
                if snake_single_location.snake_x == self.apple_x:
                    self.apple_x = random.randint(1, board[0]) // 10 * 10
                    break
                if snake_single_location.snake_y == self.apple_y:
                    self.apple_y = random.randint(1, board[0]) // 10 * 10
                    break
            break


class Apple():
    def __init__(self, snake):
        self.snake = snake
        self.apple = AppleLocation(snake)

    def draw(self):
        pygame.draw.rect(dis, blue, [self.apple.apple_x, self.apple.apple_y, 10, 10])

    def random_apple(self):
        self.apple = AppleLocation(self.snake)


class Score():
    def __init__(self):
        self.score = 0

    def add_points(self):
        self.score += 10


snake = Snake()
clock = pygame.time.Clock()
apple = Apple(snake)
score = Score()

while not game_over:
    index = 0
    for event in pygame.event.get():
        # obsługa zdarzeń
        # warunki do zmiany pozycji obiektu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake.direction != (10, 0):
                    snake.direction = (-10, 0)
                    break
            if event.key == pygame.K_RIGHT:
                if snake.direction != (-10, 0):
                    snake.direction = (10, 0)
                    break
            if event.key == pygame.K_UP:
                if snake.direction != (0, 10):
                    snake.direction = (0, -10)
                    break
            if event.key == pygame.K_DOWN:
                if snake.direction != (0, -10):
                    snake.direction = (0, 10)
                    break
    snake.update_snake()
    snake.check_colision_with_self()
    snake.check_colision_with_board()
    dis.fill(black)
    snake.draw_snake()
    apple.draw()
    snake.find_colision(apple, score)
    pygame.display.update()
    pygame.time.wait(120)
    clock.tick(60)
    print(score.score)
pygame.quit()
quit()

# kwadrat ktory chodzi
# prawo lewo gora dol, za pomoca np strzalek
# dodajemy element np tez kwadrat
# dojdziemy do niego => napisac warunek co wtedy
#   znika z dzwiekiem
#   plus waz staje sie wiekszy
#   dodatkowo pojawia sie w losowym miejscu nowy kwadrat do zjedzenia
# ramka do skucia z dzwiekiem
# menu
# licznik zyc
# poziom trudnosci
# smok ziejacy ogniem :D
