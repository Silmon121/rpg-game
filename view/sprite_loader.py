"""Module that handles sprite loading."""

import config
import pygame


class SpriteLoader:
    """Handles sprite loading."""

    def __init__(self):
        """Initialize the sprite loader."""
        self.wall_sprite = (pygame.image
                            .load(config.WOODEN_WALL_SPRITE).convert_alpha())
        self.floor_sprite = (pygame.image
                             .load(config.WOODEN_FLOOR_SPRITE).convert_alpha())
        self.player_sprite = (pygame.image
                              .load(config.PLAYER_SPRITE).convert_alpha())
