import pygame
from pygame.locals import *
import time
import random

GREEN = (0, 100, 0)

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load('python_projects-main/1_snake_game/resources/fries.jpg').convert()
        self.x, self.y = 120, 120

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(10, 18) * SIZE
        self.y = random.randint(2, 8) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('python_projects-main/1_snake_game/resources/purple.jpg').convert()
        self.x, self.y = [SIZE] * length, [SIZE] * length
        self.direction = 'right'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.y[i] = self.y[i - 1]
            self.x[i] = self.x[i - 1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

    def increase_length(self):
        self.length += 1
        self.x.append(3232)
        self.y.append(3232)


class Game:
    def __init__(self):
        pygame.init()
        self.play_background_music()
        self.surface_height = 800
        self.surface_width = 400
        self.surface = pygame.display.set_mode((self.surface_height, self.surface_width))
        self.backdrop()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.name = ''

    def main_menu(self):
        base_font = pygame.font.Font(None, 32)
        image = pygame.image.load('python_projects-main/1_snake_game/resources/snake.jpg')
        self.surface.blit(image, (0, 0))
        font = pygame.font.SysFont('verdena', 40)
        score = font.render(f'WELCOME TO THE THRILLER SNAKE GAME', True, (255, 255, 255))
        self.surface.blit(score, (80, 100))
        font = pygame.font.SysFont('verdena', 25)
        score = font.render(f'ENTER YOUR NAME', True, (255, 255, 255))
        self.surface.blit(score, (310, 180))
        text_surface = base_font.render(self.name, True, (255, 255, 255))
        self.surface.blit(text_surface, (310, 240))
        pygame.display.update()

    def backdrop(self):
        image = pygame.image.load('python_projects-main/1_snake_game/resources/439751.jpg')
        self.surface.blit(image, (0, 0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('verdena', 25)
        score = font.render(f'Name:{self.name}', True, (255, 255, 255))
        self.surface.blit(score, (80, 15))
        score = font.render(f'Score:{self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (80, 40))

    def display_game_over(self):
        self.backdrop()
        font = pygame.font.SysFont('verdena', 40)
        score = font.render(f'GAME OVER {(self.name).upper()}!', True, (255, 255, 255))
        self.surface.blit(score, (265, 130))
        score = font.render(f'YOUR SCORE: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (275, 180))
        score = font.render(f'PRESS ESC TO EXIT THE GAME', True, (255, 255, 255))
        self.surface.blit(score, (190, 230))
        pygame.display.update()

    def play(self):
        self.backdrop()
        self.snake.draw()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound('python_projects-main/1_snake_game/resources/RS6CVPT-eat-or-bite-pack.mp3')
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound('python_projects-main/1_snake_game/resources/Smash.mp3')
                pygame.mixer.Sound.play(sound)
                raise 'Game Over'

    def play_background_music(self):
        pygame.mixer.music.load('python_projects-main/1_snake_game/resources/stranger.mp3')
        pygame.mixer.music.play(-1, 0)

    def run(self):
        run = True
        pause = False
        menu = True
        while run:
            if menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            run = False
                        if event.key == K_RETURN and self.name != '':
                            menu = False
                        elif event.key == K_BACKSPACE:
                            self.name = self.name[:-1]
                        else:
                            self.name += event.unicode
                self.main_menu()
            else:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            run = False
                        if not pause:
                            if event.key == K_UP:
                                self.snake.direction = 'up'
                            if event.key == K_DOWN:
                                self.snake.direction = 'down'
                            if event.key == K_LEFT:
                                self.snake.direction = 'left'
                            if event.key == K_RIGHT:
                                self.snake.direction = 'right'
                    if event.type == pygame.QUIT:
                        run = False
                try:
                    if not pause:
                        self.play()
                except Exception as e:
                    self.display_game_over()
                    pause = True

                time.sleep(0.05)


if __name__ == '__main__':
    snake_game = Game()
    snake_game.run()
