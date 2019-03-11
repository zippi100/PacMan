import pygame
from pygame.sprite import Sprite


class Block(Sprite):
    def __init__(self, ai_settings, screen, x, y):
        super(Block, self).__init__()
        self.screen = screen
        self.width = ai_settings.block_width
        self.height = ai_settings.block_height
        self.color = ai_settings.block_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = x
        self.rect.top = y
        self.draw_rect = self.rect
        self.draw_rect.width += 1
        self.draw_rect.height += 1

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.draw_rect)


class GBlock(Sprite):
    def __init__(self, ai_settings, screen, x, y):
        super(GBlock, self).__init__()
        self.screen = screen
        self.width = ai_settings.block_width
        self.height = ai_settings.block_height
        self.color = ai_settings.dots_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = x
        self.rect.top = y
        self.draw_rect = self.rect
        self.draw_rect.width += 1
        self.draw_rect.height += 1

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.draw_rect)


class Pellet(Sprite):
    def __init__(self, ai_settings, screen, x, y):
        super(Pellet, self).__init__()
        self.screen = screen
        self.width = ai_settings.dots_width
        self.height = ai_settings.dots_height
        self.color = ai_settings.dots_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x + ai_settings.block_width/2
        self.rect.centery = y + ai_settings.block_height/2

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class PowerPellet(Sprite):
    def __init__(self, ai_settings, screen, spritesheet2, x, y):
        super(PowerPellet, self).__init__()
        self.screen = screen
        self.image_rects = ((7, 65, 19, 15), (0, 0, 1, 1))
        self.images = spritesheet2.images_at(self.image_rects, colorkey=(0, 0, 0))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = x + ai_settings.block_width/2
        self.rect.centery = y + ai_settings.block_height/2
        self.image_frame = 0

    def draw(self):
        self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self):
        self.image_frame += 1
        if self.image_frame == 2:
            self.image_frame = 0


class Maze:
    def __init__(self, ai_settings, screen, spritesheet2, blocks, g_blocks, pellets, power_pellets):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.maze = open('maze.txt', "r")
        self.mazematrix = list(self.maze)

        self.font = pygame.font.SysFont(None, 36)
        self.pre_game_image = self.font.render("READY!", True, (255, 255, 0))
        self.pre_game_image_rect = self.pre_game_image.get_rect()
        self.pre_game_image_rect.centerx = self.screen_rect.centerx
        self.pre_game_image_rect.y = self.ai_settings.block_height * 33.5 + self.ai_settings.screen_height/8

        self.create_maze(spritesheet2, blocks, g_blocks, pellets, power_pellets)

    def create_maze(self, spritesheet2, blocks, g_blocks, pellets, power_pellets):
        for y in range(0, len(self.mazematrix)):
            for x in range(0, len(self.mazematrix[y])):
                if self.mazematrix[y][x] == 'X':
                    newblock = Block(self.ai_settings, self.screen,
                                     (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                      self.ai_settings.block_width * x),
                                     self.ai_settings.block_height * y + self.ai_settings.screen_height/8)
                    blocks.add(newblock)
                elif self.mazematrix[y][x] == 'o':
                    newg_block = GBlock(self.ai_settings, self.screen,
                                        (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                         self.ai_settings.block_width * x),
                                        self.ai_settings.block_height * y + self.ai_settings.screen_height/8)
                    g_blocks.add(newg_block)
                elif self.mazematrix[y][x] == 'D':
                    newpellet = Pellet(self.ai_settings, self.screen,
                                       (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                        self.ai_settings.block_width * x),
                                       self.ai_settings.block_height * y + self.ai_settings.screen_height/8)
                    pellets.add(newpellet)
                elif self.mazematrix[y][x] == 'd':
                    newpower_pellet = PowerPellet(self.ai_settings, self.screen, spritesheet2,
                                                  (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                                   self.ai_settings.block_width * x),
                                                  self.ai_settings.block_height * y +
                                                  self.ai_settings.screen_height / 8)
                    power_pellets.add(newpower_pellet)

    def reset_maze(self, spritesheet2, pellets, power_pellets):
        for y in range(0, len(self.mazematrix)):
            for x in range(0, len(self.mazematrix[y])):
                if self.mazematrix[y][x] == 'D':
                    newpellet = Pellet(self.ai_settings, self.screen,
                                       (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                        self.ai_settings.block_width * x),
                                       self.ai_settings.block_height * y + self.ai_settings.screen_height/8)
                    pellets.add(newpellet)
                elif self.mazematrix[y][x] == 'd':
                    newpower_pellet = PowerPellet(self.ai_settings, self.screen, spritesheet2,
                                                  (self.screen_rect.centerx - self.ai_settings.block_width * 27.5 +
                                                   self.ai_settings.block_width * x),
                                                  self.ai_settings.block_height * y +
                                                  self.ai_settings.screen_height / 8)
                    power_pellets.add(newpower_pellet)

    def pre_game_draw(self):
        self.screen.blit(self.pre_game_image, self.pre_game_image_rect)
        pygame.display.flip()
