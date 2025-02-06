import math
from math import trunc

import pygame
from pygame import Surface, Vector2
import random as rd

from const import *
from sprites import *

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
            button.focus()
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
        self.on_off_button = Button(100, 100, (650, 400),'green')
    def render(self, screen):
        font = pygame.font.Font(None, 100)
        screen.blit(self.background, (0, 0))
        self.on_off_button.render(screen)
        screen.blit(font.render('Music:', 1, pygame.Color('black')), (400, 420))
    def off_on_click(self, screen):
        colot_list = {1: 'green',
                      0: 'red'}
        if self.on_off_button.flag_click(screen):
            if self.color == 1:
                self.color = 0
            else:
                self.color = 1
            self.on_off_button = Button(100, 100, (650, 400), colot_list[self.color])
            self.misic = not self.misic

class Specifications:
    def __init__(self):
        self.items = ['EYE']
        self.item_surf = Surface((1500, 250))
        self.player_spec = [100, 0, 50]
    def render(self):
        self.item_surf.fill((0, 0, 0))
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
    def enemy_render(self, enemies, pos, cletca, player_x, player_y, vis):
        font = pygame.font.Font(None, 30)
        x, y = int(pos[0] / cletca), int(pos[1] / cletca)
        if ((x, y) in enemies and x in range(player_x - vis, player_x + vis + 1)
                and y in range(player_y - vis, player_y + vis + 1)):
            self.item_surf.blit(font.render('ENEMY:', 1, pygame.Color('red')), (430, 30))
            if 'EYE' in self.items:
                self.item_surf.blit(font.render(f'HP:{enemies[x, y][0]}', 1, pygame.Color('red')), (430, 60))
                self.item_surf.blit(font.render(f'ARMOR:{enemies[x, y][1]}',1, pygame.Color('red')), (430, 90))
                self.item_surf.blit(font.render(f'ATTACK:{enemies[x, y][2]}', 1, pygame.Color('red')), (430, 120))
            else:
                self.item_surf.blit(font.render(f'HP:???', 1, pygame.Color('red')), (430, 60))
                self.item_surf.blit(font.render(f'ARMOR:???', 1, pygame.Color('red')), (430, 90))
                self.item_surf.blit(font.render(f'ATTACK:???', 1, pygame.Color('red')), (430, 120))

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
    def __init__(self, enemy):
        self.battle_field = Surface((1500, 750))
        self.battle_field.fill((0, 0, 0))
        self.en_hp = enemy[0]
        self.en_armor = enemy[1]
        self.en_attack = enemy[2]
        self.enemy_img = enemy[3]
        self.x = 750
        self.y = 600
        self.en_x = 750
        self.en_y = 100
        self.steps = rd.choice(range(1, 6))
        self.en_x_vector = rd.choice((1, -1))
        self.en_y_vector = rd.choice((1, -1))
        self.shoots = []
        self.cooldown = 0
        self.tick = 0
        self.en_cooldown = 2
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
    def enemy_move(self):
        if self.steps == 0:
            self.steps = rd.choice(range(1, 7))
            self.en_x_vector = rd.choice((1, -1))
            self.en_y_vector = rd.choice((1, -1))
        if self.en_x + 5 * self.en_x_vector > 15 and self.en_x + 5 * self.en_x_vector < 1435:
            self.en_x += 5 * self.en_x_vector
        if self.en_y + 5 * self.en_y_vector > 15 and self.en_y + 5 * self.en_y_vector < 685:
            self.en_y += 5 * self.en_y_vector
        self.steps -= 1
    def render(self, item_srf, player):
        font = pygame.font.Font(None, 30)
        self.battle_field.fill((0, 0, 0))
        pygame.draw.rect(self.battle_field, 'white', (0, 0, 1500, 750), width=5)
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
        img = pygame.transform.rotate(self.player, (self.angle * self.y_vetor * -self.x_vector) + vector_list[self.x_vector, self.y_vetor])
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
                else:
                    player[0] -= self.en_attack
                    player[1] = 0
                self.shoots.pop(cnt)
            if pygame.Rect(self.en_x, self.en_y, 50, 50).collidepoint(i[0]):
                if self.en_armor > 0:
                    self.en_armor -= player[2]
                if self.en_armor <= 0:
                    self.en_hp -= player[2]
                    self.en_armor = 0
                self.shoots.pop(cnt)
            if not(pygame.Rect(0, 0, 1500, 750).collidepoint(i[0])):
                self.shoots.pop(cnt)

            cnt += 1
        self.hp = player[0]
        if self.tick == 60:
            self.en_cooldown -= 1
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
    def player_shot(self, pos):
        if self.cooldown == 0:
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

    def enemy_shot(self):
        if self.en_cooldown == 0:
            self.en_cooldown = 2
            en_center = (self.en_x + 25, self.en_y + 25)
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    self.shoots.append([Vector2(en_center[0] + 25 * i, en_center[1] + 25 * j), Vector2(10 * i, 10 * j)])

    def end(self):
        if self.en_hp < 0:
            return 1
        elif self.hp < 0:
            return -1

class Lose:
    def __init__(self, screen):
        font = pygame.font.Font(None, 100)
        screen.blit(font.render('Вы проиграли :(', 1, pygame.Color('red')), (500, 500))
        font = pygame.font.Font(None, 20)
        screen.blit(font.render('Нажмите на пробел для продлжения', 0, pygame.Color('grey')), (650, 600))

class Win:
    def __init__(self, items, player):
        self.item = rd.choice(ITEMS)
        if self.item == 'TOCH' and 'TOUCH' not in items:
            self.text = 'Ваша вдимость увеличена на 1 клетку'
            items.append('TOUCH')
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
            self.text ='Это уже eсть у вас либо вы ничего не получили'
    def render(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        screen.blit(font.render(f'Вы получили{self.item}', 0, pygame.Color('green')), (500, 500))
        screen.blit(font.render(self.text, 0, pygame.Color('green')), (500, 550))
        screen.blit(font.render('Нажмите на пробел для продлжения', 0, pygame.Color('grey')), (500, 600))

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
if __name__ == '__main__':
    board = Playing_field()
    spec = Specifications()
    en = Enemy(MAP, 4, 1)
    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)
    fps = 60
    player = Player(board.x_pos, board.y_pos, board.cletca)
    clock = pygame.time.Clock()
    running = True
    battle = False
    playing = False
    lose_window = False
    win_window = False
    settings = False
    nasrtoiki = Settings()
    zastv = True
    zast = Zastavka()
    win = Win(spec.items, spec.player_spec)
    current_map = 0
    multipiler = 1

    move = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if zastv:
                    window = zast.open_window(position)
                    zastv = False
                    if window == 'Play':
                        playing = True
                    elif window == 'Exit':
                        running = False
                    elif window == 'Settings':
                        settings = True
                    elif window == 'Play':
                        playing = True
                elif settings:
                    nasrtoiki.off_on_click(position)
                elif battle:
                    bt.player_shot(position)
                elif playing:
                    x, y = int(position[0] / board.cletca), int(position[1] / board.cletca)
                    if board.focus and not move:
                        move = player.update(x, y, board.cletca, board.x_pos, board.y_pos, board.plaing_surf)
                        if move and en.battle_flag(x, y):
                            battle = True
                            playing = False
                            bt = Battle(en.enemy_spic[x, y])
                            en.enemy_spic.pop((x, y))
                    board.move(x, y, MAPS[current_map])
            if event.type == pygame.KEYDOWN:
                if lose_window and event.key == pygame.K_SPACE:
                    lose_window = False
                    playing = True
                elif win_window and event.key == pygame.K_SPACE:
                    win_window = False
                    playing = True
        if zastv:
            zast.render(screen)
        elif settings:
            nasrtoiki.render(screen)
        elif battle:
            bt.enemy_move()
            bt.player_move()
            bt.enemy_shot()
            spec.render()
            bt.render(spec.item_surf, spec.player_spec)
            screen.blit(bt.battle_field, (0, 0))
            screen.blit(spec.item_surf, (0, 750))
            if bt.end() == 1:
                battle = False
                win_window = True
                win = Win(spec.items, spec.player_spec)
            if bt.end() == -1:
                battle = False
                lose_window = True
        elif playing:
            spec.render()
            board.level_render(board.plaing_surf, MAPS[current_map], en.enemy_spic)
            spec.enemy_render(en.enemy_spic, pygame.mouse.get_pos(), board.cletca, board.x_pos, board.y_pos,
                                     board.visibility)
            if board.focus and not(move):
                board.focus_click(MAPS[current_map])
            if move:
                player.move()
                if player.rect.x == move[0] * board.cletca and player.rect.y == move[1] * board.cletca:
                    move = []
            if board.change_map(MAPS[current_map]):
                current_map += 1
                board = Playing_field()
                player = Player(board.x_pos, board.y_pos, board.cletca)
                multipiler += 1
                en = Enemy(MAPS[current_map], 4, multipiler)
                move = []
            screen.blit(board.plaing_surf, (0, 0))
            screen.blit(spec.item_surf, (0, 750))
            screen.blit(player.player, player.rect)
        elif lose_window:
            Lose(screen)
        elif win_window:
            win.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()