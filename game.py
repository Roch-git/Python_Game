
import pygame
from time import sleep
snake_x = 100
snake_y = 100

pygame.init()
dis = pygame.display.set_mode((400, 300))
pygame.display.update()
pygame.display.set_caption('')
game_over = False
blue = (255,0,0)
black = (0,0,0)
class SnakeLocation():
    def __init__(self, snake_x, snake_y):
       self.snake_x= snake_x
       self.snake_y= snake_y

class Snake():
    def __init__(self, rozmiar=3):
        self.snake = [SnakeLocation(snake_x, snake_y), SnakeLocation(snake_x+10, snake_y),SnakeLocation(snake_x+20, snake_y)]
        self.direction = (10,0)

    def update_snake(self):
        self.snake = self.snake[1:] + [SnakeLocation(self.snake[-1].snake_x+self.direction[0], self.snake[-1].snake_y+self.direction[1])]

    def draw_snake(self):
        for snake_single_location in self.snake:
             pygame.draw.rect(dis, blue, [snake_single_location.snake_x, snake_single_location.snake_y, 10, 10])



snake = Snake()

clock = pygame.time.Clock()
#po kliknięciu w prawo


while not game_over:
    index = 0
    for event in pygame.event.get():
        # opóźnienie w grze
        # pygame.time.delay(10)
        # obsługa zdarzeń
        # warunki do zmiany pozycji obiektu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.direction = (-10,0)
            if event.key == pygame.K_RIGHT:
                snake.direction = (10, 0)
            if event.key == pygame.K_UP:
                snake.direction = (0, -10)
            if event.key == pygame.K_DOWN:
                snake.direction = (0, 10)
            
        snake.update_snake()
        dis.fill(black)
        snake.draw_snake()
        pygame.display.update()

        clock.tick(5)
pygame.quit()
quit()

#kwadrat ktory chodzi
#prawo lewo gora dol, za pomoca np strzalek
#dodajemy element np tez kwadrat
# dojdziemy do niego => napisac warunek co wtedy
#   znika z dzwiekiem
#   plus waz staje sie wiekszy
#   dodatkowo pojawia sie w losowym miejscu nowy kwadrat do zjedzenia
# ramka do skucia z dzwiekiem
# menu
# licznik zyc
# poziom trudnosci
# smok ziejacy ogniem :D


