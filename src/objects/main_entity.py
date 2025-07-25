import pygame
from constants import *
import os


class MainEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, spritesheet="Brother64x64-Sheet.png"):
        super().__init__()
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Goes from src/objects/ → src/
        ASSET_DIR = os.path.join(BASE_DIR, "../assets/images")
        path = os.path.normpath(os.path.join(ASSET_DIR, spritesheet))

        self.spritesheet = pygame.image.load(path).convert_alpha()
        scaled_width, scaled_height = self.spritesheet.get_size()
        self.spritesheet = pygame.transform.scale(self.spritesheet, (scaled_width * 4, scaled_height * 4))

        self.x = x
        self.y = y
        self.width = w
        self.height = h

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255 ,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # self.spritesheet = Main_entity.spritesheet
        self.y_sprite_sheet_index = 0
        self.frame = 0
        self.max_frame = 3
        self.animation_speed = 10
        self.ticks_till_frame_change = self.animation_speed

    def update(self, cam_offset=0):
        self.update_cam_offset(cam_offset)
        self.animate()

    def draw(self, surface):
        image = pygame.Surface([self.rect.width, self.rect.height])
        image.fill((200, 0, 200))
        surface.blit(image, (0, 50))

    def update_cam_offset(self, cam_offset=None):
        if cam_offset:
            self.rect.x = self.x + cam_offset[0]
            self.rect.y = self.y + cam_offset[1]

    def get_image_from_sprite_sheet(self, row, col):
        if row < 0 or row > self.spritesheet.get_width():
            raise ValueError("row is either below 0 or larger than spritesheet")
        if col < 0 or col > self.spritesheet.get_height():
            raise ValueError("col is either below 0 or larger than spritesheet")

        image = pygame.Surface([self.rect.width, self.rect.height], pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (row * (self.rect.width), col  * (self.rect.height) , self.rect.width, self.rect.height))
        return image

    def animate(self):

        if self.animation_speed != 0:
            self.ticks_till_frame_change -= 1

            if self.ticks_till_frame_change <= 0:
                self.frame += 1
                self.ticks_till_frame_change = self.animation_speed  # Reset the countdown (or change as needed)
            if self.frame > self.max_frame:
                self.frame = 0
        self.image = self.get_image_from_sprite_sheet(self.frame, self.y_sprite_sheet_index)
