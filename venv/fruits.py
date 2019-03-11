import pygame
from pygame.sprite import Sprite


class Fruit(Sprite):
    def __init__(self, ai_settings, screen, spritesheet1):
        super(Fruit, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((32,128, 32, 32), (64, 128, 32, 32))

        self.images = spritesheet1.images_at(self.image_rects, colorkey=(0, 0, 0))

        self.rect = self.images[0].get_rect()

        self.rect.x = 0 - self.rect.width

        self.time = 0
        self.active = False
        self.expiration_time = 0
        self.text = False
        self.fruit_count = 0

    def update_fruit(self):
        if self.fruit_count < 2:
            self.time += 1
            if self.time == 60 * 30:
                self.rect = self.images[0].get_rect()
                self.rect.centerx = self.screen_rect.centerx
                self.rect.centery = self.ai_settings.block_height * 34.5 + self.ai_settings.screen_height/8
                self.active = True
                self.fruit_count += 1

    def draw(self, score):
        if not self.text and self.active:
            self.screen.blit(self.images[0], self.rect)
            self.expiration_time += 1
            if self.expiration_time == 60 * 10:
                self.reset_fruit()
        elif self.active:
            self.screen.blit(self.images[1], self.rect)
            self.expiration_time += 1
            if self.expiration_time == 60 * 5:
                self.reset_fruit()

    def reset_fruit(self):
            self.rect.x = 0 - self.rect.width
            self.time = 0
            self.active = False
            self.expiration_time = 0
            self.text = False

    def prep_points_image(self):
        self.rect = self.images[1].get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.ai_settings.block_height * 34.5 + self.ai_settings.screen_height / 8
        self.expiration_time = 0
