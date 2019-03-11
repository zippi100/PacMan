import pygame
from pygame.sprite import Sprite


class RedGhost(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(RedGhost, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((128, 32, 32, 32), (0, 64, 32, 32), (32, 64, 32, 32),
                            (64, 64, 32, 32), (96, 64, 32, 32), (128, 64, 32, 32),
                            (0, 96, 32, 32), (32, 96, 32, 32))

        self.images = (spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0)))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx + 64
        self.rect.y = ai_settings.screen_height/8 + ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False
        self.portal_cooldown = 0

    def check_space(self, left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                    right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                    down_collisions3, x, y, pacman, score):
        if (not left_collisions
            or (score.level > 8 and left_collisions2 and not right_collisions and pacman.portals_active))\
                and not left_collisions3 and not self.moving_left and not self.moving_right and not pacman.moving_right\
                and self.rect.x >= pacman.rect.x:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif (not right_collisions
              or (score.level > 8 and right_collisions2 and not left_collisions and pacman.portals_active))\
                and not right_collisions3 and not self.moving_right and not self.moving_left and not pacman.moving_left\
                and self.rect.x <= pacman.rect.x:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif (not up_collisions
              or (score.level > 8 and up_collisions2 and not down_collisions and pacman.portals_active))\
                and not self.moving_up and not self.moving_down and not pacman.moving_down\
                and self.rect.y >= pacman.rect.y:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif (not down_collisions
              or (score.level > 8 and down_collisions2 and not up_collisions and pacman.portals_active))\
                and not down_collisions3 and not self.moving_down and not self.moving_up and not pacman.moving_up\
                and self.rect.y <= pacman.rect.y:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6
        elif not left_collisions and not left_collisions3 and not self.moving_left and not self.moving_right:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif not right_collisions and not right_collisions3 and not self.moving_right and not self.moving_left:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif not up_collisions and not self.moving_up and not self.moving_down:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif not down_collisions and not down_collisions3 and not self.moving_down and not self.moving_up:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6

    def update_ghost(self, pacman):
        if pacman.ghost_cooldown == 0:
            if self.moving_left:
                self.rect.x -= self.ai_settings.ghost_speed
            elif self.moving_right:
                self.rect.x += self.ai_settings.ghost_speed
            elif self.moving_up:
                self.rect.y -= self.ai_settings.ghost_speed
            elif self.moving_down:
                self.rect.y += self.ai_settings.ghost_speed

    def reset_ghost(self):
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx + 64
        self.rect.y = self.ai_settings.screen_height / 8 + self.ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1

    def draw(self, pacman):
        if pacman.active:
            self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self, pacman):
        if pacman.ghost_cooldown == 0 and self.active and not self.vulnerable:
            self.image_frame += 1
            if self.moving_right and self.image_frame == 2:
                self.image_frame = 0
            elif self.moving_left and self.image_frame == 4:
                self.image_frame = 2
            elif self.moving_up and self.image_frame == 6:
                self.image_frame = 4
            elif self.moving_down and self.image_frame == 8:
                self.image_frame = 6
        elif pacman.ghost_cooldown == 0 and self.active and self.vulnerable:
            self.image_frame += 1
            if self.image_frame == 8:
                self.image_frame = 4


class GreenGhost(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(GreenGhost, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 32, 32),
                            (96, 0, 32, 32), (128, 0, 32, 32), (0, 32, 32, 32),
                            (32, 32, 32, 32), (64, 32, 32, 32))

        self.images = (spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0)))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx - 32
        self.rect.y = ai_settings.screen_height/8 + ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False
        self.portal_cooldown = 0

    def check_space(self, left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                    right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                    down_collisions3, x, y, pacman, score):
        if (not left_collisions
            or (score.level > 8 and left_collisions2 and not right_collisions and pacman.portals_active))\
                and not left_collisions3 and not self.moving_left and not self.moving_right and not pacman.moving_right\
                and self.rect.x >= pacman.rect.x:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif (not right_collisions
              or (score.level > 8 and right_collisions2 and not left_collisions and pacman.portals_active))\
                and not right_collisions3 and not self.moving_right and not self.moving_left and not pacman.moving_left\
                and self.rect.x <= pacman.rect.x:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif (not up_collisions
              or (score.level > 8 and up_collisions2 and not down_collisions and pacman.portals_active))\
                and not self.moving_up and not self.moving_down and not pacman.moving_down\
                and self.rect.y >= pacman.rect.y:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif (not down_collisions
              or (score.level > 8 and down_collisions2 and not up_collisions and pacman.portals_active))\
                and not down_collisions3 and not self.moving_down and not self.moving_up and not pacman.moving_up\
                and self.rect.y <= pacman.rect.y:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6
        elif not left_collisions and not left_collisions3 and not self.moving_left and not self.moving_right:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif not right_collisions and not right_collisions3 and not self.moving_right and not self.moving_left:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif not up_collisions and not self.moving_up and not self.moving_down:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif not down_collisions and not down_collisions3 and not self.moving_down and not self.moving_up:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6

    def update_ghost(self, pacman):
        if pacman.ghost_cooldown == 0:
            if self.moving_left:
                self.rect.x -= self.ai_settings.ghost_speed
            elif self.moving_right:
                self.rect.x += self.ai_settings.ghost_speed
            elif self.moving_up:
                self.rect.y -= self.ai_settings.ghost_speed
            elif self.moving_down:
                self.rect.y += self.ai_settings.ghost_speed

    def reset_ghost(self):
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx - 32
        self.rect.y = self.ai_settings.screen_height / 8 + self.ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1

    def draw(self, pacman):
        if pacman.active:
            self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self, pacman):
        if pacman.ghost_cooldown == 0 and self.active and not self.vulnerable:
            self.image_frame += 1
            if self.moving_right and self.image_frame == 2:
                self.image_frame = 0
            elif self.moving_left and self.image_frame == 4:
                self.image_frame = 2
            elif self.moving_up and self.image_frame == 6:
                self.image_frame = 4
            elif self.moving_down and self.image_frame == 8:
                self.image_frame = 6
        elif pacman.ghost_cooldown == 0 and self.active and self.vulnerable:
            self.image_frame += 1
            if self.image_frame == 8:
                self.image_frame = 4


class OrangeGhost(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(OrangeGhost, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((96, 32, 32, 32), (128, 32, 32, 32), (0, 64, 32, 32),
                            (32, 64, 32, 32), (64, 64, 32, 32), (96, 64, 32, 32),
                            (128, 64, 32, 32), (0, 96, 32, 32))

        self.images = (spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0)))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx + 32
        self.rect.y = ai_settings.screen_height/8 + ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False
        self.portal_cooldown = 0

    def check_space(self, left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                    right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                    down_collisions3, x, y, pacman, score):
        if (not left_collisions
            or (score.level > 8 and left_collisions2 and not right_collisions and pacman.portals_active))\
                and not left_collisions3 and not self.moving_left and not self.moving_right and not pacman.moving_right\
                and self.rect.x >= pacman.rect.x:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif (not right_collisions
              or (score.level > 8 and right_collisions2 and not left_collisions and pacman.portals_active))\
                and not right_collisions3 and not self.moving_right and not self.moving_left and not pacman.moving_left\
                and self.rect.x <= pacman.rect.x:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif (not up_collisions
              or (score.level > 8 and up_collisions2 and not down_collisions and pacman.portals_active))\
                and not self.moving_up and not self.moving_down and not pacman.moving_down\
                and self.rect.y >= pacman.rect.y:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif (not down_collisions
              or (score.level > 8 and down_collisions2 and not up_collisions and pacman.portals_active))\
                and not down_collisions3 and not self.moving_down and not self.moving_up and not pacman.moving_up\
                and self.rect.y <= pacman.rect.y:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6
        elif not left_collisions and not left_collisions3 and not self.moving_left and not self.moving_right:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif not right_collisions and not right_collisions3 and not self.moving_right and not self.moving_left:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif not up_collisions and not self.moving_up and not self.moving_down:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif not down_collisions and not down_collisions3 and not self.moving_down and not self.moving_up:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6

    def update_ghost(self, pacman):
        if pacman.ghost_cooldown == 0:
            if self.moving_left:
                self.rect.x -= self.ai_settings.ghost_speed
            elif self.moving_right:
                self.rect.x += self.ai_settings.ghost_speed
            elif self.moving_up:
                self.rect.y -= self.ai_settings.ghost_speed
            elif self.moving_down:
                self.rect.y += self.ai_settings.ghost_speed

    def reset_ghost(self):
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx + 32
        self.rect.y = self.ai_settings.screen_height / 8 + self.ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1

    def draw(self, pacman):
        if pacman.active:
            self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self, pacman):
        if pacman.ghost_cooldown == 0 and self.active and not self.vulnerable:
            self.image_frame += 1
            if self.moving_right and self.image_frame == 2:
                self.image_frame = 0
            elif self.moving_left and self.image_frame == 4:
                self.image_frame = 2
            elif self.moving_up and self.image_frame == 6:
                self.image_frame = 4
            elif self.moving_down and self.image_frame == 8:
                self.image_frame = 6
        elif pacman.ghost_cooldown == 0 and self.active and self.vulnerable:
            self.image_frame += 1
            if self.image_frame == 8:
                self.image_frame = 4


class PinkGhost(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(PinkGhost, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((32, 96, 32, 32), (64, 96, 32, 32), (96, 96, 32, 32),
                            (128, 96, 32, 32), (0, 128, 32, 32), (32, 128, 32, 32),
                            (64, 128, 32, 32), (96, 128, 32, 32))

        self.images = (spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0)))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx - 64
        self.rect.y = ai_settings.screen_height/8 + ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False
        self.portal_cooldown = 0

    def check_space(self, left_collisions, left_collisions2, left_collisions3, right_collisions, right_collisions2,
                    right_collisions3, up_collisions, up_collisions2, down_collisions, down_collisions2,
                    down_collisions3, x, y, pacman, score):
        if (not left_collisions
            or (score.level > 8 and left_collisions2 and not right_collisions and pacman.portals_active))\
                and not left_collisions3 and not self.moving_left and not self.moving_right and not pacman.moving_right\
                and self.rect.x >= pacman.rect.x:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif (not right_collisions
              or (score.level > 8 and right_collisions2 and not left_collisions and pacman.portals_active))\
                and not right_collisions3 and not self.moving_right and not self.moving_left and not pacman.moving_left\
                and self.rect.x <= pacman.rect.x:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif (not up_collisions
              or (score.level > 8 and up_collisions2 and not down_collisions and pacman.portals_active))\
                and not self.moving_up and not self.moving_down and not pacman.moving_down\
                and self.rect.y >= pacman.rect.y:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif (not down_collisions
              or (score.level > 8 and down_collisions2 and not up_collisions and pacman.portals_active))\
                and not down_collisions3 and not self.moving_down and not self.moving_up and not pacman.moving_up\
                and self.rect.y <= pacman.rect.y:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6
        elif not left_collisions and not left_collisions3 and not self.moving_left and not self.moving_right:
            self.rect.y = y
            self.rect.x -= 1
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 2
        elif not right_collisions and not right_collisions3 and not self.moving_right and not self.moving_left:
            self.rect.y = y
            self.rect.x += 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif not up_collisions and not self.moving_up and not self.moving_down:
            self.rect.x = x
            self.rect.y -= 1
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 4
        elif not down_collisions and not down_collisions3 and not self.moving_down and not self.moving_up:
            self.rect.x = x
            self.rect.y += 1
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6

    def update_ghost(self, pacman):
        if pacman.ghost_cooldown == 0:
            if self.moving_left:
                self.rect.x -= self.ai_settings.ghost_speed
            elif self.moving_right:
                self.rect.x += self.ai_settings.ghost_speed
            elif self.moving_up:
                self.rect.y -= self.ai_settings.ghost_speed
            elif self.moving_down:
                self.rect.y += self.ai_settings.ghost_speed

    def reset_ghost(self):
        self.rect = self.images[0].get_rect()
        self.rect.centerx = self.screen_rect.centerx - 64
        self.rect.y = self.ai_settings.screen_height / 8 + self.ai_settings.block_height * 21

        self.image_frame = 0
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.active = True
        self.vulnerable = False
        self.text = False

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1

    def draw(self, pacman):
        if pacman.active:
            self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self, pacman):
        if pacman.ghost_cooldown == 0 and self.active and not self.vulnerable:
            self.image_frame += 1
            if self.moving_right and self.image_frame == 2:
                self.image_frame = 0
            elif self.moving_left and self.image_frame == 4:
                self.image_frame = 2
            elif self.moving_up and self.image_frame == 6:
                self.image_frame = 4
            elif self.moving_down and self.image_frame == 8:
                self.image_frame = 6
        elif pacman.ghost_cooldown == 0 and self.active and self.vulnerable:
            self.image_frame += 1
            if self.image_frame == 8:
                self.image_frame = 4
