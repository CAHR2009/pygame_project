import math
import random as rd

import pygame
import os
import sqlite3
from pygame import Surface, Vector2, mixer

from const import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)
pygame.mixer.init()
clock = pygame.time.Clock()




def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player:
    player = load_image("player.png", colorkey=-1)
    step1 = load_image('player_step1.png', colorkey=-1)
    step2 = load_image('player_step2.png', colorkey=-1)

    def __init__(self, x, y, cletca):
        self.image = self.player
        self.rect = self.image.get_rect()
        self.rect.x = x * cletca
        self.rect.y = y * cletca
        self.cnt = 0
        self.x_vector = 0
        self.y_vector = 0
        self.angle = 0

    def update(self, map, *args):
        self.x_vector = 0
        self.y_vector = 0
        self.angle = 0
        if args[3] - 1 == args[0] and args[4] == args[1] and len(map[0]) - 1 > args[3] - 1 > 0 and len(map) - 1 > args[
            4] > 0:
            self.x_vector = -1
            self.player = pygame.transform.rotate(self.image, 270)
            self.angle = 270
        elif args[3] + 1 == args[0] and args[4] == args[1] and len(map[0]) - 1 > args[3] + 1 > 0 and len(map) - 1 > \
                args[4] > 0:
            self.x_vector = 1
            self.player = pygame.transform.rotate(self.image, 90)
            self.angle = 90
        elif args[4] - 1 == args[1] and args[3] == args[0] and len(map[0]) - 1 > args[3] > 0 and len(map) - 1 > args[
            4] - 1 > 0:
            self.y_vector = -1
            self.player = pygame.transform.rotate(self.image, 180)
            self.angle = 180
        elif args[4] + 1 == args[1] and args[3] == args[0] and len(map[0]) - 1 > args[3] > 0 and len(map) - 1 > args[
            4] + 1 > 0:
            self.y_vector = 1
            self.player = pygame.transform.rotate(self.image, 0)
            self.angle = 0
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


class Button:
    def __init__(self, wigth, height, position, color, focus_color=0):
        self.wight = wigth
        self.height = height
        self.position = position
        self.is_focus = False
        self.color = color
        self.focus_color = focus_color

    def render(self, surf):
        if self.is_focus:
            pygame.draw.rect(surf, self.focus_color, (self.position[0], self.position[1], self.wight, self.height))
        else:
            pygame.draw.rect(surf, self.color, (self.position[0], self.position[1], self.wight, self.height))

    def focus(self, pos):
        if pygame.Rect(self.position[0], self.position[1], self.wight, self.height).collidepoint(pos):
            self.is_focus = True
        else:
            self.is_focus = False

    def flag_click(self, pos):
        return pygame.Rect(self.position[0], self.position[1], self.wight, self.height).collidepoint(pos)


class Zastavka:
    background = load_image('background.png')

    def __init__(self):
            self.buttons_list = {'Play': Button(400, 100, (550, 400), (16, 124, 42), 'green'),
                             'Settings': Button(400, 100, (550, 550), (16, 124, 42), 'green'),
                             'Exit': Button(400, 100, (550, 700), (16, 124, 42), 'green'),
                             'Login': Button(250, 100, (1090, 100), 'grey', (80, 80, 80))}



    def render(self, screen):
        font = pygame.font.Font(None, 100)
        screen.blit(self.background, (0, 0))
        for key, button in self.buttons_list.items():
            button.focus(pygame.mouse.get_pos())
            button.render(screen)
            screen.blit(font.render(key, 1, pygame.Color('white')), (button.position[0] + 20, button.position[1] + 20))

    def open_window(self, pos):
        for key, button in self.buttons_list.items():
            if button.flag_click(pos):
                return key



class Settings:
    background = load_image('background.png')

    def __init__(self):
        self.misic = True
        self.color = 1
        self.on_off_button = Button(100, 100, (650, 400), 'green')
        self.exit_button = Button(200, 100, (1290, 880), (16, 124, 42), 'green')
        self.exit_to = 'Zastv'
        self.background_music = pygame.mixer.Sound('sounds/background.mp3')
        self.background_music.play(-1)
        self.background_music.set_volume(0.2)

    def render(self, screen):
        font = pygame.font.Font(None, 100)
        screen.blit(self.background, (0, 0))
        self.on_off_button.render(screen)
        self.exit_button.render(screen)
        self.exit_button.focus(pygame.mouse.get_pos())
        screen.blit(font.render('Music:', 1, pygame.Color('black')), (400, 420))
        screen.blit(font.render('Back', 1, pygame.Color('black')), (1300, 900))

    def off_on_click(self, pos):
        colot_list = {1: 'green',
                      0: 'red'}
        if self.on_off_button.flag_click(pos):
            if self.color == 1:
                self.background_music.stop()
                self.color = 0
            else:
                self.color = 1
                self.background_music.play(-1)
                self.background_music.set_volume(0.2)
            self.on_off_button = Button(100, 100, (650, 400), colot_list[self.color])
            self.misic = not self.misic

    def exit(self, pos):
        if self.exit_button.flag_click(pos):
            return self.exit_to
        else:
            return False

class Specifications:
    def __init__(self):
        self.items = []
        self.item_surf = Surface((1500, 250))
        self.player_spec = [100, 0, 50, 0]
        self.menu_button = Button(150, 50, (1150, 10), (16, 124, 42), 'green')
        self.settings_button = Button(150, 50, (1150, 70), (16, 124, 42), 'green')

    def render(self):
        self.item_surf.fill((0, 0, 0))
        font = pygame.font.Font(None, 40)
        self.menu_button.focus((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 750))
        self.settings_button.focus((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 750))
        self.menu_button.render(self.item_surf)
        self.settings_button.render(self.item_surf)
        self.item_surf.blit(font.render('MENU', 1, pygame.Color('white')), (1180, 25))
        self.item_surf.blit(font.render('SETTINGS', 1, pygame.Color('white')), (1155, 85))

        pygame.draw.rect(self.item_surf, 'white', (0, 0, 1500, 250), width=5)
        font = pygame.font.Font(None, 30)
        self.item_surf.blit(font.render('YOU:', 1, pygame.Color('green')), (30, 30))
        if self.player_spec[0] > 50:
            self.item_surf.blit(font.render(f'HP: {self.player_spec[0]}', 1, pygame.Color('green')), (30, 60))
        elif 20 < self.player_spec[0] < 50:
            self.item_surf.blit(font.render(f'HP: {self.player_spec[0]}', 1, pygame.Color('orange')), (30, 60))
        else:
            self.item_surf.blit(font.render(f'HP: {self.player_spec[0]}', 1, pygame.Color('red')), (30, 60))
        self.item_surf.blit(font.render(f'ARMOR: {self.player_spec[1]}', 1, pygame.Color('grey')), (30, 90))
        self.item_surf.blit(font.render(f'ATTACK: {self.player_spec[2]}', 1, pygame.Color('yellow')), (30, 120))
        self.item_surf.blit(font.render(f'SCORE: {self.player_spec[3]}', 1, pygame.Color('white')), (750, 30))

    def enemy_render(self, enemies, pos, cletca, player_x, player_y, vis):
        font = pygame.font.Font(None, 30)
        x, y = int(pos[0] / cletca), int(pos[1] / cletca)
        if ((x, y) in enemies and x in range(player_x - vis, player_x + vis + 1)
                and y in range(player_y - vis, player_y + vis + 1)):
            self.item_surf.blit(font.render('ENEMY:', 1, pygame.Color('red')), (430, 30))
            if 'EYE' in self.items:
                self.item_surf.blit(font.render(f'HP:{enemies[x, y][0]}', 1, pygame.Color('red')), (430, 60))
                self.item_surf.blit(font.render(f'ARMOR:{enemies[x, y][1]}', 1, pygame.Color('red')), (430, 90))
                self.item_surf.blit(font.render(f'ATTACK:{enemies[x, y][2]}', 1, pygame.Color('red')), (430, 120))
            else:
                self.item_surf.blit(font.render(f'HP:???', 1, pygame.Color('red')), (430, 60))
                self.item_surf.blit(font.render(f'ARMOR:???', 1, pygame.Color('red')), (430, 90))
                self.item_surf.blit(font.render(f'ATTACK:???', 1, pygame.Color('red')), (430, 120))
    def click(self, pos):
        if self.menu_button.flag_click(pos):
            return 'Zastv'
        elif self.settings_button.flag_click(pos):
            return 'Settings'

class Enemy:
    scorpion = load_image('scorpion.png', colorkey=-1)
    arahnid = load_image('arahnid.png', colorkey=-1)
    ant = load_image("ant.png", colorkey=-1)

    def __init__(self, map, count, multiplier):
        cnt = 0
        self.enemy_spic = {}

        while cnt != count:
            x = rd.randint(1, len(map[0]) - 1)
            y = rd.randint(1, len(map) - 1)
            enemy_armor = int(100 * rd.uniform(multiplier - 0.5, multiplier + 0.5))
            enemy_hp = int(100 * rd.uniform(multiplier - 0.5, multiplier + 0.5))
            enemy_attack = int(10 * rd.uniform(multiplier - 0.5, multiplier + 0.5))
            if map[y][x] == ' ':
                map[y] = map[y][:x] + 'e' + map[y][x + 1:]
                self.enemy_spic[x, y] = [enemy_hp, enemy_armor, enemy_attack,
                                         rd.choice([self.scorpion, self.ant, self.arahnid])]

                cnt += 1

    def battle_flag(self, x, y):
        if (x, y) in self.enemy_spic:
            return True
        return False


class Battle:
    player = load_image('player.png', colorkey=-1)
    boss = load_image('boss.png', colorkey=-1)
    battle_floor = load_image('battle_floor.png', colorkey=None)
    def __init__(self, enemy, boss_flag):
        self.battle_field = Surface((1500, 750))

        if boss_flag:
            self.en_hp = 500
            self.en_armor = 100
            self.en_attack = 99
            self.enemy_img = self.boss
            self.en_cooldown = 10
        else:
            self.en_hp = enemy[0]
            self.en_armor = enemy[1]
            self.en_attack = enemy[2]
            self.enemy_img = enemy[3]
            self.en_cooldown = 2
        self.x = 750
        self.y = 600
        self.en_x = 750
        self.en_y = 100
        self.steps = rd.choice(range(1, 6))
        self.en_x_vector = rd.choice((1, -1))
        self.en_y_vector = rd.choice((1, -1))
        self.shoots = []
        self.cooldown = 0
        self.danger_time = 5
        self.laser_attack_time = 1
        self.is_laser_attack = False
        self.tick = 0
        self.laser_pos = 0
        self.dng_color = (255, 128, 0)
        self.shoot_sound = pygame.mixer.Sound('sounds/shoot.mp3')
        self.shoot_sound.set_volume(0.2)
        self.laser_sound = pygame.mixer.Sound('sounds/laser.mp3')
        self.laser_sound.set_volume(0.2)
        self.danger_sound = pygame.mixer.Sound('sounds/danger.mp3')
        self.danger_sound.set_volume(0.2)
    def player_move(self):
        a = pygame.key.get_pressed()
        if a[pygame.K_w] and self.y > 5:
            self.y -= 10
        if a[pygame.K_s] and self.y < 645:
            self.y += 10
        if a[pygame.K_a] and self.x > 5:
            self.x -= 10
        if a[pygame.K_d] and self.x < 1445:
            self.x += 10

    def enemy_move(self, boss_flag):
        if boss_flag:
            difference = 305
        else:
            difference = 55
        if self.steps == 0:
            self.steps = rd.choice(range(1, 7))
            self.en_x_vector = rd.choice((1, -1))
            self.en_y_vector = rd.choice((1, -1))
        if self.en_x + 5 * self.en_x_vector > 15 and self.en_x + 5 * self.en_x_vector < 1500 - difference:
            self.en_x += 5 * self.en_x_vector
        if self.en_y + 5 * self.en_y_vector > 15 and self.en_y + 5 * self.en_y_vector < 750 - difference:
            self.en_y += 5 * self.en_y_vector
        self.steps -= 1

    def render(self, item_srf, player, boss_flag, music_flag):
        if boss_flag:
            hit_box = 300
        else:
            hit_box = 50
        font = pygame.font.Font(None, 30)
        self.battle_field.blit(self.battle_floor, (0, 0))
        pygame.draw.rect(self.battle_field, 'white', (0, 0, 1500, 750), width=5)

        if self.laser_pos:
            laser_srf = Surface((150, 740))
            laser_srf.set_alpha(160)
            if self.danger_time > 0 and self.en_cooldown > 0:
                laser_srf.fill(self.dng_color)
                if music_flag:
                    self.danger_sound.play(0)
            elif self.laser_attack_time > 0 and self.en_cooldown > 0:
                laser_srf.fill(('red'))
                if music_flag:
                    self.danger_sound.stop()
                    self.laser_sound.play(0)
                if not self.is_laser_attack and (
                        pygame.Rect(self.laser_pos * 50 - 50, 0, 150, 740).collidepoint(self.x, self.y) or pygame.Rect(
                        self.laser_pos * 50 - 50, 0, 150, 740).collidepoint(self.x + 50,
                                                                            self.y)):
                    self.is_laser_attack = True
                    if player[1] > 0:
                        player[1] -= self.en_attack
                        if player[1] < 0:
                            player[1] = 0
                    else:
                        player[0] -= self.en_attack
            if self.laser_attack_time or self.danger_time:
                self.battle_field.blit(laser_srf, (self.laser_pos * 50 - 50, 5))

        x, y = int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])
        vector_list = {(-1, -1): 90,
                       (-1, 1): 90,
                       (1, 1): 270,
                       (1, -1): 270}
        self.x_vector, self.y_vetor = 0, 0
        if self.x - x < 0:
            self.x_vector = -1
        else:
            self.x_vector = 1
        if self.y - y < 0:
            self.y_vetor = -1
        else:
            self.y_vetor = 1
        hupotinuse = int(math.hypot((self.x - x) * self.x_vector, (self.y - y) * self.y_vetor))
        self.angle = int(float(math.acos((self.x - x) * self.x_vector / hupotinuse) * 57.3))
        img = pygame.transform.rotate(self.player, (self.angle * self.y_vetor * -self.x_vector) + vector_list[
            self.x_vector, self.y_vetor])
        self.battle_field.blit(img, (self.x, self.y))
        self.battle_field.blit(self.enemy_img, (self.en_x, self.en_y))
        cnt = 0
        for i in self.shoots:
            pygame.draw.circle(self.battle_field, 'red',
                               i[0], 5)
            i[0] += i[1]
            if pygame.Rect(self.x, self.y, 50, 50).collidepoint(i[0]):
                if player[1] > 0:
                    player[1] -= self.en_attack
                    if player[1] < 0:
                        player[1] = 0
                else:
                    player[0] -= self.en_attack
                self.shoots.pop(cnt)
            if pygame.Rect(self.en_x, self.en_y, hit_box, hit_box).collidepoint(i[0]):
                if self.en_armor > 0:
                    self.en_armor -= player[2]
                    if self.en_armor < 0:
                        self.en_armor = 0
                else:
                    self.en_hp -= player[2]
                self.shoots.pop(cnt)
            if not (pygame.Rect(0, 0, 1500, 750).collidepoint(i[0])):
                self.shoots.pop(cnt)
            cnt += 1
        self.hp = player[0]
        if self.tick == 60:
            self.en_cooldown -= 1
            if self.laser_attack_time > 0 and self.danger_time == 0:
                self.laser_attack_time -= 1
            elif self.danger_time > 0:
                self.danger_time -= 1
                if self.danger_time % 2 == 0:
                    self.dng_color = (255, 128, 0)
                else:
                    self.dng_color = (255, 90, 0)
        if self.cooldown > 0:
            item_srf.blit(font.render(f'COOLDOWN:{self.cooldown}', 1, pygame.Color('red')), (30, 150))
            if self.tick == 60:
                self.cooldown -= 1
        else:
            item_srf.blit(font.render(f'COOLDOWN: READY', 1, pygame.Color('green')), (30, 150))


        item_srf.blit(font.render(f'HP:{self.en_hp}', 1, pygame.Color('red')), (430, 30))
        item_srf.blit(font.render(f'ARMOR:{self.en_armor}', 1, pygame.Color('red')), (430, 60))
        item_srf.blit(font.render(f'ATTACK:{self.en_attack}', 1, pygame.Color('red')), (430, 90))
        if self.tick == 60:
            self.tick = 0
        self.tick += 1

    def player_shot(self, pos, music_flag):
        if self.cooldown == 0:
            if music_flag:
                self.shoot_sound.play(0)
            rect_list = {(-1, -1): (50, 50),
                         (-1, 1): (50, 0),
                         (1, -1): (0, 50),
                         (1, 1): (0, 0)}
            self.cooldown = 1
            payer_pos = Vector2(self.x, self.y)
            mouse_pos = Vector2(*pos)
            mouse_pos -= payer_pos
            mouse_pos = mouse_pos.normalize() * 10
            mouse_pos = Vector2(round(mouse_pos.x), round(mouse_pos.y))
            self.shoots.append([Vector2(self.x + rect_list[self.x_vector, self.y_vetor][0],
                                        self.y + rect_list[self.x_vector, self.y_vetor][1]), mouse_pos])

    def enemy_shot(self, music_flag):
        if self.en_cooldown == 0:
            if music_flag:
                self.shoot_sound.play(0)
            self.en_cooldown = 2
            en_center = (self.en_x + 25, self.en_y + 25)
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    self.shoots.append([Vector2(en_center[0] + 25 * i, en_center[1] + 25 * j), Vector2(10 * i, 10 * j)])

    def boss_shot(self):
        if self.en_cooldown == 0:
            self.en_cooldown = 10
            self.danger_time = 5
            self.laser_attack_time = 1
            self.is_laser_attack = False
            self.laser_pos = rd.randint(1, 10)



    def end(self):
        if self.en_hp <= 0:
            return 1
        elif self.hp <= 0:
            return -1


class Lose:
    def __init__(self, screen):
        screen.fill((0, 0, 0))
        self.lose_sound = pygame.mixer.Sound('sounds/lose.mp3')
        self.lose_sound.set_volume(0.2)
        self.lose_sound.play(0)
        font = pygame.font.Font(None, 100)
        screen.blit(font.render('Вы проиграли :(', 1, pygame.Color('red')), (500, 500))
        font = pygame.font.Font(None, 20)
        screen.blit(font.render('Нажмите на пробел для продлжения', 0, pygame.Color('grey')), (650, 600))


class Win:
    def __init__(self, items, player, brd, music_flag):
        self.item = rd.choice(ITEMS)
        self.win_sound = pygame.mixer.Sound('sounds/bonus.mp3')
        self.win_sound.set_volume(0.2)
        self.win_sound.play(0)
        if self.item == 'TOUCH' and 'TOUCH' not in items:
            self.text = 'Ваша вдимость увеличена на 1 клетку'
            items.append('TOUCH')
            brd.visibality = 2
        elif self.item == 'HEAL':
            self.text = 'Ваше здоровье 100'
            player[0] = 100
        elif self.item == 'EYE' and 'EYE' not in items:
            self.text = 'Теперь вы видете характеристики врагов'
            items.append('EYE')
        elif self.item == 'ARMOR_UP':
            self.text = 'Ваша броня увеличена на 50'
            player[1] += 50
        elif self.item == 'ATTACK_UP':
            self.text = 'Ваша атака увеличена на 5'
            player[2] += 5
        else:
            self.text = 'Это уже eсть у вас либо вы ничего не получили'

    def render(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        screen.blit(font.render(f'Вы получили {self.item}', 0, pygame.Color('green')), (500, 500))
        screen.blit(font.render(self.text, 0, pygame.Color('green')), (500, 550))
        screen.blit(font.render('Нажмите на пробел для продлжения', 0, pygame.Color('grey')), (500, 600))

class End:
    def __init__(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        screen.blit(font.render('Вы прошли мою игру, надеюсь вам', 1,
                                pygame.Color('white')), (200, 350))
        screen.blit(font.render('понравилось :)', 1,
                                pygame.Color('white')), (500, 500))
        font = pygame.font.Font(None, 20)
        screen.blit(font.render('Нажмите на пробел для продлжения', 0, pygame.Color('grey')), (650, 600))


class Playing_field:
    # создание поля
    def __init__(self):
        self.cletca = 50
        # значения по умолчанию
        self.plaing_surf = pygame.Surface((1500, 750))
        self.focus = False
        self.x_pos = 1
        self.y_pos = 1
        self.visibility = 1

    def level_render(self, surf, map, enemies):
        wall = load_image("wall.png", colorkey=None)
        floor = load_image("floor.png", colorkey=None)
        exit_clt = load_image('exit.png', colorkey=None)
        surf.fill((0, 0, 0))
        for y_ps in range(self.y_pos - self.visibility, self.y_pos + (self.visibility + 1)):
            for x_ps in range(self.x_pos - self.visibility, self.x_pos + (self.visibility + 1)):
                if (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and map[y_ps][
                    x_ps] == ' ':
                    self.plaing_surf.blit(floor, (self.cletca * x_ps, self.cletca * y_ps))

                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and map[y_ps][
                    x_ps] == 'w':

                    self.plaing_surf.blit(wall, (self.cletca * x_ps, self.cletca * y_ps))
                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and map[y_ps][
                    x_ps] == 'p':
                    self.plaing_surf.blit(floor, (self.cletca * x_ps, self.cletca * y_ps))
                    pass
                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and map[y_ps][
                    x_ps] == 'e':
                    self.plaing_surf.blit(floor, (self.cletca * x_ps, self.cletca * y_ps))
                    self.plaing_surf.blit(enemies[x_ps, y_ps][3], (self.cletca * x_ps, self.cletca * y_ps))
                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and map[y_ps][
                    x_ps] == 'x':
                    self.plaing_surf.blit(exit_clt, (self.cletca * x_ps, self.cletca * y_ps))

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

    def change_map(self, map):
        if map[self.y_pos][self.x_pos] == map[-2][-2]:
            return True

class Login:
    background = load_image('background.png')
    def __init__(self):
        self.ok_button = Button(200, 100, (700, 500), (16, 124, 42), 'green')
        self.input_board = Button(1000, 100, (300, 350), 'grey', (80, 80, 80))
        self.back_button = Button(250, 100, (1225, 850), 'grey', (80, 80, 80))
        self.score = 0
        self.input_focus = False
        self.warning_flag = False
        self.text = ''

    def login_render(self, screen):
        font = pygame.font.Font(None, 100)
        screen.blit(self.background, (0, 0))
        if self.input_focus:
            self.input_board.is_focus = True
        else:
            self.input_board.is_focus = False
        if self.warning_flag:
            font = pygame.font.Font(None, 50)
            screen.blit(font.render('Разрешены латинские букы, цифры и символы -, _, /', 1,
                                    pygame.Color('red')), (300, 740))
        font = pygame.font.Font(None, 100)
        self.ok_button.focus(pygame.mouse.get_pos())
        self.input_board.render(screen)
        self.back_button.focus(pygame.mouse.get_pos())
        self.back_button.render(screen)
        self.ok_button.render(screen)
        screen.blit(font.render('MENU', 1, pygame.Color('white')), (1250, 870))
        screen.blit(font.render('OK', 1, pygame.Color('white')), (740, 520))
        screen.blit(font.render(self.text, 1, pygame.Color('white')), (320, 370))
        screen.blit(font.render('Введите имя до 16 символов', 1, pygame.Color('white')), (300, 220))
        screen.blit(font.render(f'Лучший счет: {self.score}', 1, pygame.Color('white')), (300, 620))


    def focus(self):
        if pygame.Rect(self.input_board.position[0], self.input_board.position[1], 1000, 100).collidepoint(
                pygame.mouse.get_pos()):
            self.input_focus = True
        else:
            self.input_focus = False
    def login_input(self, event):
        allowd_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'
            , 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        allowd_special_symbols = ['-', '_', '/', '1', '2', '3' '4' '5', '6', '7', '8', '9', '0']
        if self.input_focus and event.key == pygame.K_BACKSPACE and len(self.text):
            self.text = self.text[:-1]
        elif (self.input_focus and len(self.text) < 17 and
              (event.unicode in allowd_symbols or event.unicode in list(map(lambda x: x.upper(), allowd_symbols))
               or event.unicode in allowd_special_symbols)):
            self.text += event.unicode
        elif event.unicode not in allowd_symbols and event.unicode not in list(map(lambda x: x.upper(),
                allowd_symbols)) and event.unicode not in allowd_special_symbols:
            self.warning_flag = True

    def registration(self):
        if self.ok_button.flag_click(pygame.mouse.get_pos()):
            self.score_table = sqlite3.connect("score.db")
            self.cur = self.score_table.cursor()
            result = self.cur.execute("SELECT * FROM score_player").fetchall()
            for i in result:
                if self.text in i:
                    self.score = int(i[1])
                    return
            self.cur.execute(f"INSERT INTO score_player(Player_name, Score) VALUES('{self.text}', 0)")
            self.score_table.commit()
            self.score_table.close()
    def save_score(self, score):
        self.score_table = sqlite3.connect("score.db")
        self.cur = self.score_table.cursor()
        best_score = self.cur.execute(f"""SELECT score FROM score_player
                                            WHERE Player_name = '{self.text}'""").fetchall()

        if self.text != '' and best_score[0][0] < score:
            self.cur.execute(f"""UPDATE score_player
                            SET Score = {score}
                            WHERE Player_name = '{self.text}'""")
            print(self.text, self.score)
        self.score_table.commit()
        self.score_table.close()
    def back_to_menu(self):
        if self.back_button.flag_click(pygame.mouse.get_pos()):
            return 'Zastv'