import pygame
import pygame.font
from pygame.transform import scale


class Title:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.font = pygame.font.SysFont(None, 72)
        self.image = self.font.render(str("PacMan Portal"), True, settings.text_color, settings.bg_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = settings.screen_height * 1/8

    def draw(self):
        self.screen.blit(self.image, self.rect)


class GhostPoints:
    def __init__(self, screen, spritesheet1, spritesheet3):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.font = pygame.font.SysFont(None, 48)

        self.imagerect1 = ((32, 0, 32, 32), (32, 0, 32, 32))
        self.image1 = spritesheet1.images_at(self.imagerect1, colorkey=(0, 0, 0))

        self.imagerect2 = ((0, 0, 32, 32), (0, 0, 32, 32))
        self.image2 = spritesheet3.images_at(self.imagerect2, colorkey=(0, 0, 0))

        self.imagerect3 = ((96, 32, 32, 32), (96, 32, 32, 32))
        self.image3 = spritesheet3.images_at(self.imagerect3, colorkey=(0, 0, 0))

        self.imagerect4 = ((32, 96, 32, 32), (32, 96, 32, 32))
        self.image4 = spritesheet3.images_at(self.imagerect4, colorkey=(0, 0, 0))

        self.imagerect5 = ((128, 128, 32, 32), (128, 128, 32, 32))
        self.image5 = spritesheet3.images_at(self.imagerect5, colorkey=(0, 0, 0))

        self.rect = pygame.Rect(0, 0, 72, 72)
        self.rect.centerx, self.rect.centery = self.screen_rect.centerx, self.screen_rect.centery - 250

        self.msg_image1 = None
        self.msg_image1_rect = None
        self.msg_image2 = None
        self.msg_image2_rect = None
        self.msg_image3 = None
        self.msg_image3_rect = None
        self.msg_image4 = None
        self.msg_image4_rect = None
        self.msg_image5 = None
        self.msg_image5_rect = None
        self.imagerect = self.rect

        self.prep_msg("= PacMan", "= Inky", "= Clyde", "= Pinky", "= Blinky")

    def prep_msg(self, msg1, msg2, msg3, msg4, msg5):
        self.msg_image1 = self.font.render(msg1, True, (255, 247, 0), (0, 0, 0))
        self.msg_image1_rect = self.msg_image1.get_rect()
        self.msg_image1_rect.left, self.msg_image1_rect.centery = self.rect.centerx, self.rect.centery
        self.msg_image2 = self.font.render(msg2, True, (0, 233, 255), (0, 0, 0))
        self.msg_image2_rect = self.msg_image2.get_rect()
        self.msg_image2_rect.left, self.msg_image2_rect.centery = self.rect.centerx, self.msg_image1_rect.centery + 72
        self.msg_image3 = self.font.render(msg3, True, (217, 96, 0), (0, 0, 0))
        self.msg_image3_rect = self.msg_image3.get_rect()
        self.msg_image3_rect.left, self.msg_image3_rect.centery = self.rect.centerx, self.msg_image2_rect.centery + 72
        self.msg_image4 = self.font.render(msg4, True, (240, 0, 255), (0, 0, 0))
        self.msg_image4_rect = self.msg_image4.get_rect()
        self.msg_image4_rect.left, self.msg_image4_rect.centery = self.rect.centerx, self.msg_image3_rect.centery + 72

        self.msg_image5 = self.font.render(msg5, True, (255, 0, 0), (0, 0, 0))
        self.msg_image5_rect = self.msg_image5.get_rect()
        self.msg_image5_rect.left, self.msg_image5_rect.centery = self.rect.centerx, self.msg_image4_rect.centery + 72

    def draw(self):
        self.screen.blit(self.msg_image1, self.msg_image1_rect)
        self.imagerect.right, self.imagerect.centery = self.msg_image1_rect.left - 5, self.msg_image1_rect.centery
        self.screen.blit(scale(self.image1[0], (72, 72)), self.imagerect)
        self.screen.blit(self.msg_image2, self.msg_image2_rect)
        self.imagerect.centery = self.msg_image2_rect.centery
        self.screen.blit(scale(self.image2[0], (72, 72)), self.imagerect)
        self.screen.blit(self.msg_image3, self.msg_image3_rect)
        self.imagerect.centery = self.msg_image3_rect.centery
        self.screen.blit(scale(self.image3[0], (72, 72)), self.imagerect)
        self.screen.blit(self.msg_image4, self.msg_image4_rect)
        self.imagerect.centery = self.msg_image4_rect.centery
        self.screen.blit(scale(self.image4[0], (72, 72)), self.imagerect)
        self.screen.blit(self.msg_image5, self.msg_image5_rect)
        self.imagerect.centery = self.msg_image5_rect.centery
        self.screen.blit(scale(self.image5[0], (72, 72)), self.imagerect)
