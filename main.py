from random import random

import pygame
from pygame import Surface
import random as rd

from const import *
from sprites import *

class Enemy:
    def __init__(self, map, count, multiplier):
        cnt = 0
        self.enemy_spic = {}

        while cnt != count:
            x = rd.randint(1, len(map[0]) - 1)
            y = rd.randint(1, len(map) - 1)
            enemy_armor = int(100 * rd.uniform(multiplier - 0.5, multiplier + 0.5))
            enemy_hp = int(100 * rd.uniform(multiplier - 0.5, multiplier + 0.5))
            if map[y][x] == ' ':
                map[y] = map[y][:x] + 'e' + map[y][x + 1:]
                self.enemy_spic[x, y] = [enemy_hp, enemy_armor]
                print(self.enemy_spic)
                print(*map, sep='\n')
                cnt += 1


class Specifications:
    def __init__(self):
        self.items = []
        self.item_surf = Surface((1500, 250))
        self.hp = 100
        self.armor = 0

class  Playing_field:
    # создание поля
    def __init__(self):
        self.cletca = 50
        # значения по умолчанию
        self.plaing_surf = pygame.Surface((1500, 750))
        self.focus = False
        self.x_pos = 1
        self.y_pos = 1
        self.visibility = 2

    def level_render(self, surf, map):
        wall = load_image("wall.png", colorkey=None)
        floor = load_image("floor.png", colorkey=None)
        surf.fill((0, 0, 0))
        for y_ps in range(self.y_pos - self.visibility, self.y_pos + (self.visibility + 1)):
            for x_ps in range(self.x_pos - self.visibility, self.x_pos + (self.visibility + 1)):
                if (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == ' ':
                    self.plaing_surf.blit(floor, (self.cletca * x_ps, self.cletca * y_ps))

                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == 'w':

                    self.plaing_surf.blit(wall, (self.cletca * x_ps, self.cletca * y_ps))
                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == 'p':
                    self.plaing_surf.blit(floor, (self.cletca * x_ps, self.cletca * y_ps))
                    pass
    def focus_click(self, map):
        green = load_image('green.png', colorkey=-1)
        clt = self.cletca
        if self.x_pos + 2 < len(map[1]):
            self.plaing_surf.blit(green, ((self.x_pos + 1) * clt, self.y_pos * clt))
        if self.x_pos - 1 > 0:
            self.plaing_surf.blit(green, ((self.x_pos - 1) * clt, self.y_pos * clt))
        if self.y_pos + 2 < len(map):
            self.plaing_surf.blit(green, (self.x_pos * clt, (self.y_pos + 1) * clt))
        if self.y_pos - 1 > 0:
            self.plaing_surf.blit(green, (self.x_pos * clt, (self.y_pos - 1) * clt))
        self.focus = True
    def move(self, x, y, map):
        if x == self.x_pos and y == self.y_pos:
            self.focus = not (self.focus)
        if self.focus:
            if x == self.x_pos - 1 and y == self.y_pos and x > 0:
                map[y] = map[y].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.x_pos -= 1
                self.focus = False

            elif x == self.x_pos + 1 and y == self.y_pos and x < len(map[0]) - 1:
                map[y] = map[y].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.x_pos += 1
                self.focus = False


            elif y == self.y_pos - 1 and x == self.x_pos and y > 0:
                map[y + 1] = map[y + 1].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.y_pos -= 1
                self.focus = False

            elif y == self.y_pos + 1 and x == self.x_pos and y < len(map) - 1:
                map[y - 1] = map[y - 1].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.y_pos += 1
                self.focus = False
            elif x == self.x_pos and y == self.y_pos:
                pass
            else:
                self.focus = False

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    pygame.init()
    board = Playing_field()
    player_spec = Specifications()
    Enemy(MAP, 2, 1)
    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)
    fps = 60
    player = Player(board.x_pos, board.y_pos, board.cletca)
    clock = pygame.time.Clock()
    running = True
    move = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                x, y = int(position[0] / board.cletca), int(position[1] / board.cletca)
                if board.focus and not(move):
                    move = player.update(x, y, board.cletca, board.x_pos, board.y_pos, board.plaing_surf)
                    pass
                board.move(x, y, MAP)
        board.level_render(board.plaing_surf, MAP)
        if board.focus and not(move):
            board.focus_click(MAP)
        if move:
            player.move()
            if player.rect.x == move[0] * board.cletca and player.rect.y == move[1] * board.cletca:
                move = []
        screen.blit(board.plaing_surf, (0, 0))
        screen.blit(player_spec.item_surf, (0, 750))
        screen.blit(player.player, player.rect)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()