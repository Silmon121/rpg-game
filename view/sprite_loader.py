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
        self.light_elf_sprite = (pygame.image
                              .load(config.LIGHT_ELF_SPRITE).convert_alpha())
        self.goal_door_sprite = (pygame.image
                              .load(config.GOAL_DOOR_SPRITE).convert_alpha())
        self.goal_door_locked_sprite = (pygame.image
                                 .load(config.GOAL_DOOR_LOCKED_SPRITE).convert_alpha())
        self.sword_sprite = (pygame.image
                              .load(config.SWORD_SPRITE).convert_alpha())