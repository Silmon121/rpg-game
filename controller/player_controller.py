"""
Player input controller module.

Handles keyboard input and translates it into
player movement actions.
"""

import pygame
import registry


class PlayerController:
    """
    Translates input events into player actions.

    Responsibilities:
        - Reads keyboard input
        - Moves player entity accordingly
    """

    @staticmethod
    def handle_input(event):
        """
        Process a pygame input event and move the player.

        Args:
            event: pygame event containing key input
        """
        player = registry.game.player

        # Safety check: ensure player position exists
        if player.x is None and player.y is None:
            return

        match event.key:
            case pygame.K_w:
                player.move(0, -1)
            case pygame.K_s:
                player.move(0, 1)
            case pygame.K_a:
                player.move(-1, 0)
            case pygame.K_d:
                player.move(1, 0)
