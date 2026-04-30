"""
Player input controller module.

Handle keyboard input and translate it into player actions.
"""

import pygame
from model import Sword


class PlayerController:
    """
    Handle player input and state updates.

    Translate input events into movement and combat actions.
    """

    def __init__(self, game_controller):
        """
        Initialize PlayerController instance.

        Parameters
        ----------
        game_controller : GameController
                Controller providing access to player, entities, and systems.
        """
        self.gc = game_controller

    def handle_input(self, event):
        """
        Process input event and update player actions.

        Parameters
        ----------
        event : pygame.event.Event
            Input event containing key information.
        """
        player = self.gc.player

        if player is None:
            return

        # Ensure player position exists
        if player.x is None and player.y is None:
            return

        if not player.sword_attack:
            match event.key:
                case pygame.K_w:
                    player.move(0, -1)
                case pygame.K_s:
                    player.move(0, 1)
                case pygame.K_a:
                    player.move(-1, 0)
                case pygame.K_d:
                    player.move(1, 0)
                case pygame.K_SPACE:
                    self.sword_attack()

    def check_player_status(self, dt):
        """
        Update player-related state.

        Handle player death and active weapon entities.

        Parameters
        ----------
        dt : float
            Time delta used for updating cooldowns.
        """
        player = self.gc.player

        if player is None:
            return

        if player.health <= 0:
            self.gc.restart_level()

        if player.sword_attack:
            for entity in self.gc.entities[:]:
                if isinstance(entity, Sword):
                    if entity.update(dt):
                        self.gc.entities.remove(entity)
                        player.sword_attack = False

    def sword_attack(self):
        """
        Trigger sword attack action.

        Spawn a sword entity in front of the player and
        perform initial collision checks.
        """
        player = self.gc.player

        player.sword_attack = True

        self.gc.create_entity(
            "sword",
            x=player.face_direction[0] + player.x,
            y=player.face_direction[1] + player.y,
        )

        swords = [
            entity for entity in self.gc.entities
            if isinstance(entity, Sword)
        ]

        for sword in swords:
            self.gc.cc.check_collision(sword.x, sword.y, sword)
