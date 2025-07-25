from constants import *
import pygame
import random
from event_system import event_system

class MenuStable():
    def __init__(self):
        from player.player import main_player
        self.player = main_player.current_wrestler.battle_object
        # self.items = self.player.options["Items"]
        self.player_group = pygame.sprite.Group()
        for wrestler in main_player.stable:
            self.player_group.add(wrestler.battle_object)
        self.player.rect.topleft = (0, 0)
        self.index = 0


    def update(self):
        self.player_group.update()
        # self.index = self.index % len(self.items)


    def draw(self, surface):
        WIDTH, HEIGHT = surface.get_size()
        font_size = 20
        padding = 20
        text_padding = 10

        font = pygame.font.SysFont("Arial", font_size)

        main_w = BLOCK_SIZE * 10 + padding * 3
        main_h = BLOCK_SIZE * len(self.player_group) * 2 + padding * 5
        main_x = WIDTH // 2 - main_w // 2
        main_y = HEIGHT // 2 - main_h // 2

        main_box = info_box = pygame.Rect(main_x, main_y, main_w, main_h)
        pygame.draw.rect(surface, (0, 200, 0), main_box)

        avatar_spacing = BLOCK_SIZE * SCALE / 2
        for i, wrestler in enumerate(self.player_group):
            X = main_box.left + padding
            Y = main_box.top + avatar_spacing * i + padding * i + padding
            wrestler.rect.topleft = (X, Y)
            self.draw_scaled(wrestler, surface)

            x = main_x + avatar_spacing + padding * 3
            y = Y + padding
            w = BLOCK_SIZE * 3
            h = font_size * 4 + padding
            name_box = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, BLACK, name_box, 3)
            info = [
                f"Name:{wrestler.name}",
                f"Class:{wrestler.type_class}",
                f"HP:{wrestler.hp} / {wrestler.max_hp}",
                f"MP:{wrestler.mp} / {wrestler.max_mp}"
            ]

            for index, i in enumerate(info):
                text = font.render(i, True, BLACK)
                surface.blit(text, (name_box.x + text_padding, name_box.y + text_padding + index * font_size))

            x = name_box.right + padding
            y = name_box.top
            w = BLOCK_SIZE * 4 + padding
            h = name_box.height

            stat_names = ["Level", "Exp", "Speed", "Power", "Defense", "Technique", "Charisma", "Luck"]
            l = len(stat_names)
            info_box = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, BLACK, info_box, 3)
            for index, stat in enumerate(wrestler.stats):
                text = font.render(f"{stat_names[index]}: {stat}", True, BLACK)
                if index < 4:
                    surface.blit(text, (info_box.x + text_padding, info_box.y + text_padding + index * font_size))
                else:
                    surface.blit(text, (info_box.x + text_padding + (font_size * 6), info_box.y + text_padding + (index - 4) * font_size))

    def draw_scaled(self, sprite, surface):
        scale = 0.5
        scaled_image = pygame.transform.scale(sprite.image, (
            int(sprite.rect.width * scale),
            int(sprite.rect.height * scale)
        ))
        rect = scaled_image.get_rect(topleft=sprite.rect.topleft)
        surface.blit(scaled_image, rect)
