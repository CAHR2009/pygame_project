
import pygame
import os
import sys


pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    player = load_image("player.png", colorkey=-1)
    step1 = load_image('player_step1.png', colorkey=-1)
    step2 = load_image('player_step2.png', colorkey=-1)
    def __init__(self, x, y, cletca):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.image = self.player
        self.rect = self.image.get_rect()
        self.rect.x = x * cletca
        self.rect.y = y * cletca
        self.cnt = 0
        self.x_vector = 0
        self.y_vector = 0
    def update(self, *args):
        self.x_vector = 0
        self.y_vector = 0
        self.angle = 0
        if args[3] - 1 == args[0] and args[4] == args[1]:
            self.x_vector = -1
            self.player = pygame.transform.rotate(self.image, 270)
            self.angle = 270
        elif args[3] + 1 == args[0] and args[4] == args[1]:
            self.x_vector = 1
            self.player = pygame.transform.rotate(self.image, 90)
            self.angle = 90
        if args[4] - 1 == args[1] and args[3] == args[0]:
            self.y_vector = -1
            self.player = pygame.transform.rotate(self.image, 180)
            self.angle = 180
        elif args[4] + 1 == args[1] and args[3] == args[0]:
            self.y_vector = 1
            self.player = pygame.transform.rotate(self.image, 0)
            self.angle = 0
        print(self.x_vector, self.x_vector)
        if self.x_vector or self.y_vector:
            return [args[0], args[1]]
        return False
    def move(self):
        spic = [self.step1, self.step2]
        if self.cnt > 1:
            self.cnt = 0
        self.player = pygame.transform.rotate(spic[self.cnt], self.angle)
        self.cnt += 1
        self.rect.x += 5 * self.x_vector
        self.rect.y += 5 * self.y_vector
        clock.tick(10)

class Button(pygame.sprite.Sprite):
    pass