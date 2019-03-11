import pygame
from pygame.sprite import Group
from PacMan import Pacman


class Score:
    def __init__(self, ai_settings, screen, spritesheet1):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.spritesheet1 = spritesheet1

        self.level = 1
        self.points = 0
        self.lives = 3
        self.extra_life_tracker = 0
        self.pacmans = None
        self.text_color = ai_settings.text_color
        self.bg_color = ai_settings.bg_color
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.high_score = None
        self.high_score_file = open("High_Scores.txt", "r")
        self.high_score_list = []
        for line in self.high_score_file:
            self.high_score_list.append(int(line))
        self.high_score_file.close()
        if self.high_score_list:
            self.high_score = self.high_score_list[0]
        else:
            self.high_score = 0

        self.score_image1 = self.font.render("SCORE", True, self.text_color, self.bg_color)
        self.image_rect1 = self.score_image1.get_rect()
        self.image_rect1.centerx = self.screen_rect.centerx
        self.image_rect1.y = 0

        self.high_score_image1 = self.font.render("HIGH SCORE", True, self.text_color, self.bg_color)
        self.image_rect3 = self.high_score_image1.get_rect()
        self.image_rect3.right = self.screen_rect.right
        self.image_rect3.y = 0

        self.level_image1 = self.font.render("LEVEL", True, self.text_color, self.bg_color)
        self.image_rect5 = self.level_image1.get_rect()
        self.image_rect5.left = self.screen_rect.left
        self.image_rect5.y = 0

        self.score_image2 = None
        self.image_rect2 = None
        self.high_score_image2 = None
        self.image_rect4 = None
        self.level_image2 = None
        self.image_rect6 = None

        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        self.score_image2 = self.font.render(str(self.points), True, self.text_color, self.bg_color)
        self.image_rect2 = self.score_image2.get_rect()
        self.image_rect2.centerx = self.screen_rect.centerx
        self.image_rect2.y = 24

    def show_score(self):
        self.screen.blit(self.score_image1, self.image_rect1)
        self.screen.blit(self.score_image2, self.image_rect2)

    def prep_high_score(self):
        if self.points > self.high_score:
            self.high_score = self.points
        self.high_score_image2 = self.font.render(str(self.high_score), True, self.text_color, self.bg_color)
        self.image_rect4 = self.high_score_image2.get_rect()
        self.image_rect4.right = self.screen_rect.right
        self.image_rect4.y = 24

    def show_high_score(self):
        self.screen.blit(self.high_score_image1, self.image_rect3)
        self.screen.blit(self.high_score_image2, self.image_rect4)

    def prep_level(self):
        self.level_image2 = self.font.render(str(self.level), True, self.text_color, self.bg_color)
        self.image_rect6 = self.level_image2.get_rect()
        self.image_rect6.left = self.screen_rect.left
        self.image_rect6.y = 24

    def show_level(self):
        self.screen.blit(self.level_image1, self.image_rect5)
        self.screen.blit(self.level_image2, self.image_rect6)

    def prep_lives(self):
        self.pacmans = Group()
        for x in range(self.lives):
            new_pacman = Pacman(self.ai_settings, self.screen, self.spritesheet1)
            new_pacman.rect.x = (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                 self.ai_settings.entity_width * x * 1.5)
            new_pacman.rect.y = self.ai_settings.block_height * 61 + self.ai_settings.screen_height/8 + 1
            self.pacmans.add(new_pacman)

    def show_lives(self):
        for life in self.pacmans:
            self.screen.blit(life.images[1], life.rect)

    def reset_score(self):
        self.points = 0
        self.lives = 3
        self.extra_life_tracker = 0

    def show_high_score_list(self):
        for x in range(0, len(self.high_score_list)):
            self.rect.x, self.rect.y = self.screen_rect.centerx - 60, self.screen_rect.centery / 3 + 10 + x * 48
            self.screen.blit(self.font.render((str(x + 1) + ".   " + str(self.high_score_list[x])), True,
                                              self.text_color, (0, 0, 0)), self.rect)

    def update_score(self, points):
        self.points += points
        self.extra_life_tracker += points

    def extra_life(self):
        if self.extra_life_tracker >= 10000:
            self.lives += 1
            self.extra_life_tracker = self.extra_life_tracker % 10000
            self.prep_lives()
