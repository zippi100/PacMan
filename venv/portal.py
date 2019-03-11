import pygame
from pygame.sprite import Sprite


class PortalBullet(Sprite):
    def __init__(self, ai_settings, screen, spritesheet2, pacman):
        super(PortalBullet, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.imagerects = ((69, 42, 5, 5), (82, 42, 5, 5), (76, 39, 5, 5), (77, 45, 5, 5),
                           (37, 43, 5, 5), (52, 41, 5, 5), (43, 36, 6, 6), (44, 44, 6, 6))
        self.images = spritesheet2.images_at(self.imagerects, colorkey=(0, 0, 0))
        self.current_image = None

        self.rect = self.images[0].get_rect()

        self.speed = ai_settings.bullet_speed
        self.direction = pacman.direction
        self.portal_switch = pacman.portal_switch
        self.pacman_rect = pacman.rect

        self.initialize_bullet()

    def initialize_bullet(self):
        if self.direction == 0:
            self.rect.right = self.pacman_rect.left
            self.rect.centery = self.pacman_rect.centery
            if not self.portal_switch:
                self.current_image = self.images[0]
            else:
                self.current_image = self.images[4]
        elif self.direction == 1:
            self.rect.left = self.pacman_rect.right
            self.rect.centery = self.pacman_rect.centery
            if not self.portal_switch:
                self.current_image = self.images[1]
            else:
                self.current_image = self.images[5]
        elif self.direction == 2:
            self.rect.bottom = self.pacman_rect.top
            self.rect.centerx = self.pacman_rect.centerx
            if not self.portal_switch:
                self.current_image = self.images[2]
            else:
                self.current_image = self.images[6]
        elif self.direction == 3:
            self.rect.top = self.pacman_rect.bottom
            self.rect.centerx = self.pacman_rect.centerx
            if not self.portal_switch:
                self.current_image = self.images[3]
            else:
                self.current_image = self.images[7]

    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def update_bullet(self):
        if self.direction == 0:
            self.rect.x -= self.speed
        elif self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == 3:
            self.rect.y += self.speed

    def regress(self):
        if self.direction == 0:
            self.rect.x += 1
        elif self.direction == 1:
            self.rect.x -= 1
        elif self.direction == 2:
            self.rect.y += 1
        elif self.direction == 3:
            self.rect.y -= 1


class Portal(Sprite):
    def __init__(self, ai_settings, screen, spritesheet2):
        super(Portal, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.imagerects1 = ((42, 0, 10, 30), (12, 0, 9, 30))
        self.imagerects2 = ((0, 40, 33, 15), (66, 10, 28, 11))
        self.images = spritesheet2.images_at(self.imagerects1, colorkey=(0, 0, 0))
        self.images.extend(spritesheet2.images_at(self.imagerects2, colorkey=(0, 0, 0)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x -= self.rect.width
        self.portal_direction = None

        self.portal_active = False
        self.expiration_time = 0

    def initialize_portal(self, bullet, portal_switch):
        if bullet.direction == 0 or bullet.direction == 1:
            if not portal_switch:
                self.image = self.images[0]
            else:
                self.image = self.images[1]
            self.rect = self.image.get_rect()
            if bullet.direction == 0:
                self.portal_direction = 1
                self.rect.right = bullet.rect.left
            else:
                self.portal_direction = 0
                self.rect.left = bullet.rect.right
            self.rect.centery = bullet.rect.centery
        if bullet.direction == 2 or bullet.direction == 3:
            if not portal_switch:
                self.image = self.images[2]
            else:
                self.image = self.images[3]
            self.rect = self.image.get_rect()
            if bullet.direction == 2:
                self.portal_direction = 3
                self.rect.bottom = bullet.rect.top
            else:
                self.portal_direction = 2
                self.rect.top = bullet.rect.bottom
            self.rect.centerx = bullet.rect.centerx
        self.portal_active = True
        self.expiration_time = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def reset_portal(self, pacman):
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x -= self.rect.width
        self.portal_direction = None
        self.portal_active = False
        self.expiration_time = 0
        pacman.portals_active = False

    def expire_portal(self, pacman):
        if self.portal_active:
            self.expiration_time += 1
            if self.expiration_time == 60 * 10:
                self.reset_portal(pacman)


class SidePortals:
    def __init__(self, ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.left_x = self.screen_rect.centerx - self.ai_settings.block_width * 30.5
        self.right_x = self.screen_rect.centerx + self.ai_settings.block_width * 27.5
        self.y = self.ai_settings.block_height * 27 + self.ai_settings.screen_height * 1/8 + 1
        self.left_rect = pygame.Rect(self.left_x, self.y, ai_settings.entity_width, ai_settings.entity_height)
        self.right_rect = pygame.Rect(self.right_x, self.y, ai_settings.entity_width, ai_settings.entity_height)
        self.color = (0, 0, 0)

    def draw(self):
        self.screen.fill(self.color, self.left_rect)
        self.screen.fill(self.color, self.right_rect)

    def transport(self, entity):
        if entity.rect.left <= self.left_rect.left:
            entity.rect.right = self.right_rect.right - 1
        elif entity.rect.right >= self.right_rect.right:
            entity.rect.left = self.left_rect.left + 1
