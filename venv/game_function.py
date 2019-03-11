import pygame
from pygame.sprite import Group
from time import sleep
import sys
from portal import PortalBullet


def check_keydown_events(event, ai_settings, screen, spritesheet2, pacman, bullets):
    if event.key == pygame.K_LEFT:
        pacman.move_left = True
    elif event.key == pygame.K_RIGHT:
        pacman.move_right = True
    elif event.key == pygame.K_UP:
        pacman.move_up = True
    elif event.key == pygame.K_DOWN:
        pacman.move_down = True
    elif event.key == pygame.K_SPACE:
        if not pacman.bullet_active:
            bullet = PortalBullet(ai_settings, screen, spritesheet2, pacman)
            bullets.add(bullet)
            pacman.bullet_active = True


def check_keyup_events(event, pacman):
    if event.key == pygame.K_LEFT:
        pacman.move_left = False
    elif event.key == pygame.K_RIGHT:
        pacman.move_right = False
    elif event.key == pygame.K_UP:
        pacman.move_up = False
    elif event.key == pygame.K_DOWN:
        pacman.move_down = False


def check_events(ai_settings, screen, spritesheet2, play_button, score_button, pacman, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and ai_settings.game_on:
            check_keydown_events(event, ai_settings, screen, spritesheet2, pacman, bullets)
        if event.type == pygame.KEYUP and ai_settings.game_on:
            check_keyup_events(event, pacman)
        if event.type == pygame.MOUSEBUTTONDOWN and not ai_settings.game_on:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, play_button, pacman, mouse_x, mouse_y)
            check_score_button(ai_settings, score_button, mouse_x, mouse_y)


def check_play_button(ai_settings, play_button, pacman, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        ai_settings.game_on = True
        pacman.reset_pacman()


def check_score_button(ai_settings, score_button, mouse_x, mouse_y):
    clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
    if clicked and not ai_settings.score_on:
        ai_settings.score_on = True
        score_button.msg = 'BACK'
        score_button.prep_msg()
    elif clicked and ai_settings.score_on:
        ai_settings.score_on = False
        score_button.msg = 'HIGH SCORES'
        score_button.prep_msg()


def check_collisions(ai_settings, score, pacman, blocks, g_blocks, pellets, power_dots,
                     left_hitbox, right_hitbox, up_hitbox, down_hitbox, bullets, red_portal, blue_portal, fruit,
                     side_portals, red_ghost, green_ghost, orange_ghost, pink_ghost):
    pacmans = Group()
    pacmans.add(pacman)
    portals = Group()
    portals.add(red_portal)
    portals.add(blue_portal)

    pacman_collisions(ai_settings, score, blocks, g_blocks, pellets, power_dots, pacman, pacmans, left_hitbox,
                      right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, fruit,
                      side_portals)

    ghost_collisions(ai_settings, score, blocks, g_blocks, pacman, left_hitbox,
                     right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, side_portals, red_ghost)
    ghost_collisions(ai_settings, score, blocks, g_blocks, pacman, left_hitbox,
                     right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, side_portals, green_ghost)
    ghost_collisions(ai_settings, score, blocks, g_blocks, pacman, left_hitbox,
                     right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, side_portals, orange_ghost)
    ghost_collisions(ai_settings, score, blocks, g_blocks, pacman, left_hitbox,
                     right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, side_portals, pink_ghost)

    bullet_collisions(pacman, blocks, g_blocks, bullets, red_portal, blue_portal, portals, side_portals)

    if not pacman.active:
        sleep(1)
        fruit.reset_fruit()
        fruit.fruit_count = 0
        bullets.empty()
        red_portal.reset_portal(pacman)
        blue_portal.reset_portal(pacman)

    score.prep_score()
    score.prep_high_score()


def end_level(ai_settings, screen, time, spritesheet2, score, title, play_button, score_button,
              pacman, maze, blocks, g_blocks, dots, power_dots, bullets, red_portal, blue_portal, fruit,
              side_portals, red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost):
    maze.reset_maze(spritesheet2, dots, power_dots)
    pacman.reset_pacman()
    red_ghost.reset_ghost()
    green_ghost.reset_ghost()
    orange_ghost.reset_ghost()
    pink_ghost.reset_ghost()
    fruit.reset_fruit()
    fruit.fruit_count = 0
    bullets.empty()
    red_portal.reset_portal(pacman)
    blue_portal.reset_portal(pacman)
    sleep(2)
    ai_settings.level_up(score)
    score.prep_level()
    update_screen(ai_settings, screen, time, score, play_button, title, score_button, pacman, blocks, g_blocks, dots,
                  power_dots, bullets, red_portal, blue_portal, fruit, side_portals, red_ghost, ghostpoints,
                  green_ghost, orange_ghost, pink_ghost)
    maze.pre_game_draw()
    sleep(3)


def pacman_collisions(ai_settings, score, blocks, g_blocks, dots, power_dots, pacman, pacmans, left_hitbox,
                      right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, fruit, side_portals):
    left_hits = Group()
    left_hits.add(left_hitbox)
    right_hits = Group()
    right_hits.add(right_hitbox)
    up_hits = Group()
    up_hits.add(up_hitbox)
    down_hits = Group()
    down_hits.add(down_hitbox)

    side_portals.transport(pacman)

    current_position, next_position = None, None
    if pacman.moving_left:
        current_position, next_position = pacman.rect.x - ai_settings.pacman_speed, pacman.rect.x
    elif pacman.moving_right:
        current_position, next_position = pacman.rect.x, pacman.rect.x + ai_settings.pacman_speed
    elif pacman.moving_up:
        current_position, next_position = pacman.rect.y - ai_settings.pacman_speed, pacman.rect.y
    elif pacman.moving_down:
        current_position, next_position = pacman.rect.y, pacman.rect.y + ai_settings.pacman_speed

    collisions1 = pygame.sprite.groupcollide(pacmans, dots, False, True)
    collisions2 = pygame.sprite.groupcollide(pacmans, power_dots, False, True)
    collisions3 = pygame.sprite.collide_rect(pacman, fruit)
    red_portal_collision = pygame.sprite.collide_rect(pacman, red_portal)
    blue_portal_collision = pygame.sprite.collide_rect(pacman, blue_portal)

    if collisions1:
        for dots in collisions1.values():
            score.update_score(ai_settings.dots_value * len(dots))
    if collisions2:
        for power_dots in collisions2.values():
            score.update_score(ai_settings.power_dots_value * len(power_dots))
    if collisions3 and not fruit.text:
        fruit.text = True
        score.update_score(100)
        fruit.prep_points_image()

    if pacman.moving_left or pacman.moving_right:
        for x in range(current_position, next_position):
            up_hitbox.rect.x = x
            down_hitbox.rect.x = x
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
            left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
            left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
            right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
            right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
            up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
            down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
            down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
            pacman.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                               right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                               down_collisions3, x, pacman.rect.y)
    elif pacman.moving_up or pacman.moving_down:
        for y in range(current_position, next_position):
            left_hitbox.rect.y = y
            right_hitbox.rect.y = y
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
            left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
            left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
            right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
            right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
            up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
            down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
            down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
            pacman.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                               right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                               down_collisions3, pacman.rect.x, y)
    else:
        left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
        left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
        left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
        right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
        right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
        right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
        up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
        up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
        down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
        down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
        down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
        pacman.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                           right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                           down_collisions3, pacman.rect.x, pacman.rect.y)

    left_hitbox.update_hitbox(pacman)
    right_hitbox.update_hitbox(pacman)
    up_hitbox.update_hitbox(pacman)
    down_hitbox.update_hitbox(pacman)

    left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
    left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
    right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
    right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
    up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
    up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
    down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
    down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)

    if red_portal_collision:
        if pacman.portal_cooldown == 0:
            portal_transfer(pacman, blue_portal)
    elif blue_portal_collision:
        if pacman.portal_cooldown == 0:
            portal_transfer(pacman, red_portal)
    elif left_collisions and not (left_collisions2 and pacman.portals_active) and pacman.moving_left:
        while left_collisions:
            pacman.left_block_collide()
            left_hitbox.update_hitbox(pacman)
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
        pacman.rect.x -= 2
    elif right_collisions and not (right_collisions2 and pacman.portals_active) and pacman.moving_right:
        while right_collisions:
            pacman.right_block_collide()
            right_hitbox.update_hitbox(pacman)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
        pacman.rect.x += 2
    elif up_collisions and not (up_collisions2 and pacman.portals_active) and pacman.moving_up:
        while up_collisions:
            pacman.up_block_collide()
            up_hitbox.update_hitbox(pacman)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
        pacman.rect.y -= 2
    elif down_collisions and not (down_collisions2 and pacman.portals_active) and pacman.moving_down:
        while down_collisions:
            pacman.down_block_collide()
            down_hitbox.update_hitbox(pacman)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
        pacman.rect.y += 2


def ghost_collisions(ai_settings, score, blocks, g_blocks, pacman, left_hitbox,
                     right_hitbox, up_hitbox, down_hitbox, red_portal, blue_portal, portals, side_portals, ghost):
    left_hitbox.rect.right = ghost.rect.left - 3
    left_hitbox.rect.top = ghost.rect.top
    right_hitbox.rect.left = ghost.rect.right + 3
    right_hitbox.rect.top = ghost.rect.top
    up_hitbox.rect.left = ghost.rect.left
    up_hitbox.rect.bottom = ghost.rect.top - 3
    down_hitbox.rect.left = ghost.rect.left
    down_hitbox.rect.top = ghost.rect.bottom + 3

    left_hits = Group()
    left_hits.add(left_hitbox)
    right_hits = Group()
    right_hits.add(right_hitbox)
    up_hits = Group()
    up_hits.add(up_hitbox)
    down_hits = Group()
    down_hits.add(down_hitbox)

    side_portals.transport(ghost)

    current_position, next_position = None, None
    if ghost.moving_left:
        current_position, next_position = ghost.rect.x - ai_settings.ghost_speed, ghost.rect.x
    elif ghost.moving_right:
        current_position, next_position = ghost.rect.x, ghost.rect.x + ai_settings.ghost_speed
    elif ghost.moving_up:
        current_position, next_position = ghost.rect.y - ai_settings.ghost_speed, ghost.rect.y
    elif ghost.moving_down:
        current_position, next_position = ghost.rect.y, ghost.rect.y + ai_settings.ghost_speed

    if ghost.moving_left or ghost.moving_right:
        for x in range(current_position, next_position):
            up_hitbox.rect.x = x
            down_hitbox.rect.x = x
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
            left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
            left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
            right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
            right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
            up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
            down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
            down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
            ghost.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                              right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                              down_collisions3, x, ghost.rect.y, pacman, score)
    elif ghost.moving_up or ghost.moving_down:
        for y in range(current_position, next_position):
            left_hitbox.rect.y = y
            right_hitbox.rect.y = y
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
            left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
            left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
            right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
            right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
            up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
            down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
            down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
            ghost.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                              right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                              down_collisions3, ghost.rect.x, y, pacman, score)
    else:
        left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
        left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
        left_collisions3 = pygame.sprite.groupcollide(left_hits, g_blocks, False, False)
        right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
        right_collisions3 = pygame.sprite.groupcollide(right_hits, g_blocks, False, False)
        right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
        up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
        up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
        down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
        down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
        down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
        ghost.check_space(left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                          right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                          down_collisions3, ghost.rect.x, ghost.rect.y, pacman, score)

    left_hitbox.update_hitbox(ghost)
    right_hitbox.update_hitbox(ghost)
    up_hitbox.update_hitbox(ghost)
    down_hitbox.update_hitbox(ghost)

    red_portal_collision = pygame.sprite.collide_rect(ghost, red_portal)
    blue_portal_collision = pygame.sprite.collide_rect(ghost, blue_portal)
    pacman_collision = pygame.sprite.collide_rect(ghost, pacman)

    if pacman_collision:
        pacman.active = False
        pacman.image_frame = 12
    elif red_portal_collision:
        if ghost.portal_cooldown == 0:
            portal_transfer(ghost, blue_portal)
    elif blue_portal_collision:
        if ghost.portal_cooldown == 0:
            portal_transfer(ghost, red_portal)


def portal_transfer(pacman, exit_portal):
    if exit_portal.portal_direction == 0:
        pacman.rect.right = exit_portal.rect.right
        pacman.rect.y = exit_portal.rect.y
        pacman.direction = 0
        pacman.moving_left = True
        pacman.moving_right = False
        pacman.moving_up = False
        pacman.moving_down = False
        pacman.image_frame = 4
    elif exit_portal.portal_direction == 1:
        pacman.rect.left = exit_portal.rect.left
        pacman.rect.y = exit_portal.rect.y
        pacman.direction = 1
        pacman.moving_left = False
        pacman.moving_right = True
        pacman.moving_up = False
        pacman.moving_down = False
        pacman.image_frame = 1
    elif exit_portal.portal_direction == 2:
        pacman.rect.bottom = exit_portal.rect.bottom
        pacman.rect.x = exit_portal.rect.x
        pacman.direction = 2
        pacman.moving_up = True
        pacman.moving_down = False
        pacman.moving_left = False
        pacman.moving_right = False
        pacman.image_frame = 7
    elif exit_portal.portal_direction == 3:
        pacman.rect.top = exit_portal.rect.top
        pacman.rect.x = exit_portal.rect.x
        pacman.direction = 3
        pacman.moving_up = False
        pacman.moving_down = True
        pacman.moving_left = False
        pacman.moving_right = False
        pacman.image_frame = 9
    pacman.portal_cooldown = int(pacman.ai_settings.block_width/pacman.ai_settings.pacman_speed + 1)


def bullet_collisions(pacman, blocks, g_blocks, bullets, red_portal, blue_portal, portals, side_portals):
    collisions1 = pygame.sprite.groupcollide(blocks, bullets, False, False)
    collisions2 = pygame.sprite.groupcollide(portals, bullets, False, False)
    copy_portal_rect = None
    copy_portal_image = None

    for bullet in bullets:
        side_portals.transport(bullet)
    if collisions2:
        bullets.empty()
        pacman.bullet_active = False
    elif collisions1:
        while collisions1:
            for bullet in bullets:
                bullet.regress()
            collisions1 = pygame.sprite.groupcollide(blocks, bullets, False, False)
        for bullet in bullets:
            if not pacman.portal_switch:
                copy_portal_rect = red_portal.rect
                copy_portal_image = red_portal.image
                red_portal.initialize_portal(bullet, pacman.portal_switch)
            else:
                copy_portal_rect = blue_portal.rect
                copy_portal_image = blue_portal.image
                blue_portal.initialize_portal(bullet, pacman.portal_switch)
        portals.empty()
        portals.add(red_portal)
        portals.add(blue_portal)
        collisions3 = pygame.sprite.groupcollide(portals, g_blocks, False, False)
        bullets.empty()
        pacman.bullet_active = False
        if not collisions3:
            if not pacman.portal_switch:
                pacman.portal_switch = True
            else:
                pacman.portal_switch = False
            if red_portal.portal_active and blue_portal.portal_active:
                pacman.portals_active = True
        else:
            if not pacman.portal_switch:
                red_portal.rect = copy_portal_rect
                red_portal.image = copy_portal_image
            else:
                blue_portal.rect = copy_portal_rect
                blue_portal.image = copy_portal_image


def update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks, g_blocks, dots,
                  power_dots, bullets, red_portal, blue_portal, fruit, side_portals, red_ghost, ghostpoints,
                  green_ghost, orange_ghost, pink_ghost):
    if not ai_settings.game_on and not ai_settings.score_on:
        screen.fill(ai_settings.bg_color)
        title.draw()
        ghostpoints.draw()
        play_button.prep_msg()
        score_button.prep_msg()
        play_button.draw()
        score_button.draw()
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            play_button.prep_msg_highlight()
            play_button.draw_highlight()
        elif score_button.rect.collidepoint(pygame.mouse.get_pos()):
            score_button.prep_msg_highlight()
            score_button.draw_highlight()
    elif ai_settings.game_on:
        screen.fill(ai_settings.bg_color)
        draw_maze(blocks, g_blocks, dots, power_dots)
        fruit.draw(score)
        pacman.draw()
        red_ghost.draw(pacman)
        green_ghost.draw(pacman)
        orange_ghost.draw(pacman)
        pink_ghost.draw(pacman)
        for bullet in bullets:
            bullet.draw()
        red_portal.draw()
        blue_portal.draw()
        side_portals.draw()
        score.show_score()
        score.show_high_score()
        score.show_level()
        score.show_lives()
        if time % 3 == 0 and pacman.active:
            pacman.next_frame()
            red_ghost.next_frame(pacman)
            green_ghost.next_frame(pacman)
            orange_ghost.next_frame(pacman)
            pink_ghost.next_frame(pacman)
        elif time % 6 == 0 and not pacman.active:
            pacman.next_frame()
        if time % 30 == 0:
            for power_dot in power_dots:
                power_dot.next_frame()
    elif ai_settings.score_on:
        screen.fill(ai_settings.bg_color)
        score.show_high_score_list()
        score_button.prep_msg()
        score_button.draw()
        if score_button.rect.collidepoint(pygame.mouse.get_pos()):
            score_button.prep_msg_highlight()
            score_button.draw_highlight()
    pygame.display.flip()


def draw_maze(blocks, g_blocks, dots, power_dots):
    for block in blocks.sprites():
        block.draw()
    for g_block in g_blocks.sprites():
        g_block.draw()
    for dot in dots.sprites():
        dot.draw()
    for power_dot in power_dots.sprites():
        power_dot.draw()
