import pygame.ftfont


class Button:
    def __init__(self, ai_settings, screen, msg, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x = x
        self.y = y
        self.width, self.height = 200, 50
        self.button_color = ai_settings.button_color
        self.text_color = ai_settings.text_color
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.centery = y

        self.msg = msg
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.x
        self.msg_rect.centery = self.y

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.x
        self.msg_rect.centery = self.y

    def prep_msg_highlight(self):
        self.msg_image = self.font.render(self.msg, True, self.button_color, self.text_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.x
        self.msg_rect.centery = self.y

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)

    def draw_highlight(self):
        self.screen.fill(self.text_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)
