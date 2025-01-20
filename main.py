import pygame
from const import *



class  Playing_field:
    # создание поля
    def __init__(self):
        self.cletca = 25
        # значения по умолчанию
        self.plaing_surf = pygame.Surface((1500, 750))
        self.focus = False
        self.x_pos = 1
        self.y_pos = 1
        self.visibility = 1

    def level_render(self, surf, map):
        surf.fill((0, 0, 0))
        for y_ps in range(self.y_pos - self.visibility, self.y_pos + (self.visibility + 1)):
            for x_ps in range(self.x_pos - self.visibility, self.x_pos + (self.visibility + 1)):
                if (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == ' ':
                    pygame.draw.rect(surf, 'white', (self.cletca * x_ps, self.cletca * y_ps,
                                                       self.cletca, self.cletca), width=1)

                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == 'w':
                    pygame.draw.rect(surf, 'red', (self.cletca * x_ps, self.cletca * y_ps,
                                                       self.cletca, self.cletca))

                elif (y_ps >= 0 and y_ps <= len(map) - 1) and (x_ps >= 0 and x_ps <= len(map[0]) - 1) and MAP[y_ps][
                    x_ps] == 'p':
                    pygame.draw.rect(surf, 'blue', (self.x_pos * self.cletca, self.y_pos * self.cletca,
                                                               self.cletca, self.cletca))
    def focus_click(self, map):
        clt = self.cletca
        if self.x_pos + 2 < len(map[1]):
            pygame.draw.rect(self.plaing_surf, 'green', ((self.x_pos + 1) * clt, self.y_pos * clt, clt, clt))
        if self.x_pos - 1 > 0:
            pygame.draw.rect(self.plaing_surf, 'green', ((self.x_pos - 1) * clt, self.y_pos * clt, clt, clt))
        if self.y_pos + 2 < len(map):
            pygame.draw.rect(self.plaing_surf, 'green', (self.x_pos * clt, (self.y_pos + 1) * clt, clt, clt))
        if self.y_pos - 1 > 0:
            pygame.draw.rect(self.plaing_surf, 'green', (self.x_pos * clt, (self.y_pos - 1) * clt, clt, clt))
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

            elif y == self.y_pos - 1 and x == self.x_pos and y > 1:
                map[y + 1] = map[y + 1].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.y_pos -= 1
                self.focus = False

            elif y == self.y_pos + 1 and x == self.x_pos and y < len(map) - 1:
                map[y - 1] = map[y - 1].replace('p', ' ')
                map[y] = map[y][:x] + 'p' + map[y][x + 1:]
                self.y_pos += 1
                self.focus = False
            elif x == board.x_pos and y == board.y_pos:
                pass
            else:
                board.focus = False


if __name__ == '__main__':
    pygame.init()
    board = Playing_field()
    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                x, y = int(position[0] / board.cletca), int(position[1] / board.cletca)
                board.move(x, y, MAP)

        pygame.display.flip()
        board.level_render(board.plaing_surf, MAP)
        if board.focus:
            board.focus_click(MAP)
        screen.blit(board.plaing_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()