import config
import pygame

class SpriteLoader:
    def __init__(self):
        self.wall_sprite = pygame.image.load(config.WOODEN_WALL_SPRITE).convert_alpha()
        self.floor_sprite = pygame.image.load(config.WOODEN_FLOOR_SPRITE).convert_alpha()
        self.player_sprite = pygame.image.load(config.PLAYER_SPRITE).convert_alpha()