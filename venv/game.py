import pygame
from pygame.sprite import Group
from settings import Settings
from title import Title
from spritesheets import SpriteSheet
from button import Button
from scoreboard import Score
from PacMan import Pacman
from PacMan import LeftHitbox
from PacMan import RightHitbox
from PacMan import UpHitbox
from PacMan import DownHitbox
from time import sleep
from ghost import RedGhost
from ghost import GreenGhost
from ghost import OrangeGhost
from ghost import PinkGhost
from portal import Portal
from portal import SidePortals
from fruits import Fruit
from maze import Maze
import game_function as gf
from title import GhostPoints


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("PacMan Portal")
    spritesheet1 = SpriteSheet('PacManNGhost.png', screen)
    spritesheet2 = SpriteSheet('MoreStuff.png', screen)
    spritesheet3 = SpriteSheet('Ghost.png', screen)
    title = Title(ai_settings, screen)
    ghostpoints = GhostPoints(screen, spritesheet1, spritesheet3)

    play_button = Button(ai_settings, screen, "Play", ai_settings.screen_width/2, ai_settings.screen_height*2/3)
    score_button = Button(ai_settings, screen, "High Scores", ai_settings.screen_width/2,
                          ai_settings.screen_height*2/3 + 100)

    score = Score(ai_settings, screen, spritesheet1)

    pacman = Pacman(ai_settings, screen, spritesheet1)
    red_ghost = RedGhost(ai_settings, screen, spritesheet1)
    green_ghost = GreenGhost(ai_settings, screen, spritesheet3)
    orange_ghost = OrangeGhost(ai_settings, screen, spritesheet3)
    pink_ghost = PinkGhost(ai_settings, screen, spritesheet3)

    red_portal = Portal(ai_settings, screen, spritesheet2)
    blue_portal = Portal(ai_settings, screen, spritesheet2)

    left_hitbox = LeftHitbox(ai_settings, pacman)
    right_hitbox = RightHitbox(ai_settings, pacman)
    up_hitbox = UpHitbox(ai_settings, pacman)
    down_hitbox = DownHitbox(ai_settings, pacman)

    blocks = Group()
    g_blocks = Group()
    dots = Group()
    power_dots = Group()
    bullets = Group()
    side_portals = SidePortals(ai_settings, screen)
    fruit = Fruit(ai_settings, screen, spritesheet1)
    time = 1

    maze = Maze(ai_settings, screen, spritesheet2, blocks, g_blocks, dots, power_dots)

    while True:

        timer = pygame.time.Clock()
        timer.tick(60)
        time += 1
        if time == 61:
            time = 1
        gf.update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks, g_blocks,
                         dots, power_dots, bullets, red_portal, blue_portal, fruit, side_portals,
                         red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)

        gf.check_events(ai_settings, screen, spritesheet2, play_button, score_button, pacman, bullets)
        if ai_settings.game_on:
            pygame.mouse.set_visible(False)
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
            score.reset_score()
            score.prep_lives()
            score.prep_score()
            score.prep_high_score()
            score.prep_level()
            gf.update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                             g_blocks, dots, power_dots, bullets, red_portal, blue_portal, fruit, side_portals,
                             red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)
            maze.pre_game_draw()

            sleep(5)
            while ai_settings.game_on:
                timer.tick(60)
                time += 1
                if time == 61:
                    time = 1
                pacman.cooldown()
                red_ghost.cooldown()
                green_ghost.cooldown()
                orange_ghost.cooldown()
                pink_ghost.cooldown()
                gf.check_events(ai_settings, screen, spritesheet2, play_button, score_button, pacman, bullets)
                if pacman.active:
                    gf.check_collisions(ai_settings, score, pacman, blocks, g_blocks, dots, power_dots, left_hitbox,
                                        right_hitbox, up_hitbox, down_hitbox, bullets, red_portal, blue_portal,
                                        fruit, side_portals, red_ghost, green_ghost, orange_ghost, pink_ghost)
                score.extra_life()

                if not pacman.active and score.lives > 0:
                    score.lives -= 1
                    score.prep_lives()
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
                    sleep(3)
                    gf.update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                     g_blocks, dots, power_dots, bullets, red_portal, blue_portal, fruit,
                                     side_portals, red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)
                    maze.pre_game_draw()
                    sleep(5)
                elif not pacman.active and score.lives == 0:
                    sleep(3)
                    ai_settings.game_on = False
                    pygame.mouse.set_visible(True)
                    for x in range(0, len(score.high_score_list)):
                        if score.points > score.high_score_list[x]:
                            score.high_score_list.insert(x, score.points)
                            score.high_score_list.pop()
                            break
                    high_score_file = open("High_Scores.txt", "w")
                    for x in range(0, len(score.high_score_list) - 1):
                        high_score_file.write(str(score.high_score_list[x]) + "\n")
                    high_score_file.write(str(score.high_score_list[8]))
                    high_score_file.close()
                    print(list(map(str, score.high_score_list)))

                pacman.update_pacman()
                red_ghost.update_ghost(pacman)
                green_ghost.update_ghost(pacman)
                orange_ghost.update_ghost(pacman)
                pink_ghost.update_ghost(pacman)
                for bullet in bullets:
                    bullet.update_bullet()
                left_hitbox.update_hitbox(pacman)
                right_hitbox.update_hitbox(pacman)
                up_hitbox.update_hitbox(pacman)
                down_hitbox.update_hitbox(pacman)
                red_portal.expire_portal(pacman)
                blue_portal.expire_portal(pacman)
                fruit.update_fruit()

                gf.update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                 g_blocks, dots, power_dots, bullets, red_portal, blue_portal, fruit,
                                 side_portals, red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)

                if len(dots) == 0 and len(power_dots) == 0:
                    gf.end_level(ai_settings, screen, time, spritesheet2, score, title, play_button, score_button,
                                 pacman,
                                 maze, blocks, g_blocks, dots, power_dots, bullets, red_portal, blue_portal,
                                 fruit, side_portals, red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)
        elif ai_settings.score_on:
            while ai_settings.score_on:
                gf.check_events(ai_settings, screen, spritesheet2, play_button, score_button, pacman, bullets)
                gf.update_screen(ai_settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                 g_blocks, dots, power_dots, bullets, red_portal, blue_portal, fruit,
                                 side_portals, red_ghost, ghostpoints, green_ghost, orange_ghost, pink_ghost)


run_game()
