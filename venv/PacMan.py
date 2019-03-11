import pygame
from pygame.sprite import Sprite


class Pacman(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(Pacman, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 32, 32),
                            (0, 0, 32, 32), (96, 0, 32, 32), (128, 0, 32, 32),
                            (0, 0, 32, 32), (0, 32, 32, 32), (32, 32, 32, 32),
                            (0, 0, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32),
                            (0, 0, 32, 32), (96, 128, 32, 32), (128, 128, 32, 32),
                            (0, 150, 32, 32), (32, 150, 32, 32), (64, 150, 32, 32),
                            (96, 150, 32, 32), (128, 150, 32, 32))

        self.images = spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0))

        self.rect = self.images[0].get_rect()
        self.rect.y = self.ai_settings.block_height * 45 + self.ai_settings.screen_height * 1/8
        self.rect.centerx = self.screen_rect.centerx

        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.moving_up = False
        self.direction = 1

        self.active = True
        self.bullet_active = False
        self.portals_active = False
        self.portal_switch = False
        self.portal_cooldown = 0
        self.ghost_cooldown = 0

        self.image_frame = 1

    def check_space(self, left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                    right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                    down_collisions3, x, y):
        if (not left_collisions or (left_collisions2 and not right_collisions)) and not left_collisions3 and \
                self.move_left and not self.moving_left and self.active:
            self.direction = 0
            self.rect.y = y
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 4
        elif (not right_collisions or (right_collisions2 and not left_collisions)) and not right_collisions3 and\
                self.move_right and not self.moving_right and self.active:
            self.direction = 1
            self.rect.y = y
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 1
        elif (not up_collisions or (up_collisions2 and not down_collisions)) and self.move_up and not self.moving_up:
            self.direction = 2
            self.rect.x = x
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 7
        elif (not down_collisions or (down_collisions2 and not up_collisions)) and not down_collisions3 and \
                self.move_down and not self.moving_down and self.active:
            self.direction = 3
            self.rect.x = x
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 9

    def left_block_collide(self):
        self.moving_left = False
        self.rect.x += 1

    def right_block_collide(self):
        self.moving_right = False
        self.rect.x -= 1

    def up_block_collide(self):
        self.moving_up = False
        self.rect.y += 1

    def down_block_collide(self):
        self.moving_down = False
        self.rect.y -= 1

    def update_pacman(self):
        if self.ghost_cooldown == 0 and self.active:
            if self.moving_left:
                self.rect.x -= self.ai_settings.pacman_speed
            elif self.moving_right:
                self.rect.x += self.ai_settings.pacman_speed
            elif self.moving_up:
                self.rect.y -= self.ai_settings.pacman_speed
            elif self.moving_down:
                self.rect.y += self.ai_settings.pacman_speed

    def reset_pacman(self):
        self.rect.y = self.ai_settings.block_height * 45 + self.ai_settings.screen_height * 1/8 + 1
        self.rect.centerx = self.screen_rect.centerx

        self.active = True
        self.direction = 1
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.moving_up = False

        self.image_frame = 1

    def draw(self):
        if self.ghost_cooldown == 0:
            self.screen.blit(self.images[self.image_frame], self.rect)
        else:
            self.ghost_cooldown -= 1

    def next_frame(self):
        if self.ghost_cooldown == 0:
            if (self.moving_left or self.moving_right or self.moving_up or self.moving_down) and self.active:
                self.image_frame += 1
                if self.image_frame == 3 and self.moving_right:
                    self.image_frame = 0
                elif self.image_frame == 6 and self.moving_left:
                    self.image_frame = 3
                elif self.image_frame == 9 and self.moving_up:
                    self.image_frame = 6
                elif self.image_frame == 12 and self.moving_down:
                    self.image_frame = 9
            elif not self.active and self.image_frame < 20:
                self.image_frame += 1

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1


class LeftHitbox(Sprite):
    def __init__(self, ai_settings, pacman):
        super(LeftHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, 1, ai_settings.entity_height)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.right = pacman.rect.left - 1
        self.rect.top = pacman.rect.top


class RightHitbox(Sprite):
    def __init__(self, ai_settings, pacman):
        super(RightHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, 1, ai_settings.entity_height)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.right + 2
        self.rect.top = pacman.rect.top


class UpHitbox(Sprite):
    def __init__(self, ai_settings, pacman):
        super(UpHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, ai_settings.entity_width, 1)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.left
        self.rect.bottom = pacman.rect.top - 1


class DownHitbox(Sprite):
    def __init__(self, ai_settings, pacman):
        super(DownHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, ai_settings.entity_width, 1)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.left
        self.rect.top = pacman.rect.bottom + 2
