from os.path import split

import pygame

from classes import *



def start_game():
    global player, running, battle, playing, lose_window, win_window, settings, \
        nastroiki, zastv, zast, win, current_map, multipiler, board, spec, en, move, maps, boss_battle, main_window
    board = Playing_field()
    spec = Specifications()
    multipiler = 1
    current_map = 4
    maps = [i.copy() for i in MAPS.copy()]
    en = Enemy(maps[current_map], current_map + 1, multipiler)
    player = Player(board.x_pos, board.y_pos, board.cletca)
    main_window = 'Zastv'
    running = True
    move = []

def menu():
    global window, main_window
    window = spec.click((position[0], position[1] - 750))
    if window:
        if window == 'Settings':
            main_window = 'Settings'
            nastroiki.exit_to = 'Play'
        else:
            main_window = 'Zastv'
            start_game()

if __name__ == '__main__':
    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)
    fps = 60
    zast = Zastavka()
    nastroiki = Settings()
    login = Login()
    clock = pygame.time.Clock()
    start_game()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if main_window == 'Zastv':
                    window = zast.open_window(position)
                    if window == 'Settings':
                        nastroiki.exit_to = 'Zastv'
                        main_window = window
                    elif window == 'Exit':
                        running = False
                    elif window:
                        main_window = window
                elif main_window == 'Settings':
                    nastroiki.off_on_click(position)
                    if nastroiki.exit(position):
                        main_window = nastroiki.exit_to
                elif main_window == 'Battle':
                    bt.player_shot(position, nastroiki.misic)
                    menu()
                    nastroiki.exit_to = 'Battle'
                elif main_window == 'Boss_battle':
                    boss_bt.player_shot(position, nastroiki.misic)
                    menu()
                    nastroiki.exit_to = 'Boss_battle'
                elif main_window == 'Login':
                    login.focus()
                    login.registration()
                    window = login.back_to_menu()
                    if window:
                        main_window = window
                elif main_window == 'Play':
                    x, y = int(position[0] / board.cletca), int(position[1] / board.cletca)
                    if board.focus and not move:
                        move = player.update(maps[current_map], x, y, board.cletca, board.x_pos, board.y_pos, board.plaing_surf)
                        if move and en.battle_flag(x, y):
                            main_window = 'Battle'
                            bt = Battle(en.enemy_spic[x, y], False)
                            en.enemy_spic.pop((x, y))
                    board.move(x, y, maps[current_map])
                    window = spec.click((position[0], position[1] - 750))
                    menu()
            if event.type == pygame.KEYDOWN:
                if main_window == 'Lose' and event.key == pygame.K_SPACE:
                    main_window = 'Zastv'
                    start_game()
                elif main_window == 'Win' and event.key == pygame.K_SPACE:
                    main_window = 'Play'
                elif main_window == 'End' and event.key == pygame.K_SPACE:
                    start_game()
                elif main_window == 'Login':
                    login.login_input(event)
        if main_window == 'Zastv':
            zast.render(screen)
        elif main_window == 'Settings':
            nastroiki.render(screen)
        elif main_window == 'Battle':
            bt.enemy_move(False)
            bt.player_move()
            bt.enemy_shot(nastroiki.misic)
            spec.render()
            bt.render(spec.item_surf, spec.player_spec, False)
            screen.blit(bt.battle_field, (0, 0))
            screen.blit(spec.item_surf, (0, 750))
            if bt.end() == 1:
                main_window = 'Win'
                win = Win(spec.items, spec.player_spec, board, nastroiki.misic)
                if win.item == 'TOUCH':
                    board.visibility = 2
                spec.player_spec[3] += 10
            if bt.end() == -1:
                main_window = 'Lose'
        elif main_window == 'Play':
            spec.render()
            board.level_render(board.plaing_surf, maps[current_map], en.enemy_spic)
            spec.enemy_render(en.enemy_spic, pygame.mouse.get_pos(), board.cletca, board.x_pos, board.y_pos,
                                     board.visibility)
            if board.focus and not(move):
                board.focus_click(maps[current_map])
            if move:
                player.move()
                if player.rect.x == move[0] * board.cletca and player.rect.y == move[1] * board.cletca:
                    move = []
            if board.change_map(maps[current_map]):
                if current_map < 4:
                    current_map += 1
                    board = Playing_field()
                    if 'TOUCH' in spec.items:
                        board.visibility = 2
                    player = Player(board.x_pos, board.y_pos, board.cletca)
                    multipiler += 0.5
                    en = Enemy(maps[current_map], current_map + 1, multipiler)
                    move = []
                else:
                    main_window = 'Boss_battle'
                    boss_bt = Battle([], True)
            screen.blit(board.plaing_surf, (0, 0))
            screen.blit(spec.item_surf, (0, 750))
            screen.blit(player.player, player.rect)
        elif main_window == 'Lose':
            Lose(screen)
            login.save_score(spec.player_spec[3])
        elif main_window == 'Win':
            win.render(screen)
        elif main_window == 'End':
            End(screen)
        elif main_window == 'Boss_battle':
            boss_bt.enemy_move(True)
            boss_bt.player_move()
            spec.render()
            boss_bt.boss_shot()
            boss_bt.render(spec.item_surf, spec.player_spec, True, nastroiki.misic)
            screen.blit(boss_bt.battle_field, (0, 0))
            screen.blit(spec.item_surf, (0, 750))
            if boss_bt.end() == 1:
                login.save_score(spec.player_spec[3])
                main_window = 'End'
            if boss_bt.end() == -1:
                main_window = 'Lose'
                login.save_score(spec.player_spec[3])
        elif main_window == 'Login':
            login.login_render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()