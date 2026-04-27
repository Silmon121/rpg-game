"""
Player input controller module.

Handles keyboard input and translates it into
player movement actions.
"""

import pygame
from model.entities.objects.weapons.sword import Sword


class PlayerController:
    """
    Translates input events into player actions.

    Responsibilities:
        - Reads keyboard input
        - Moves player entity accordingly
    """

    def __init__(self, game_controller):
        self.gc = game_controller

    def handle_input(self, event):
        """
        Process a pygame input event and move the player.

        Args:
            event: pygame event containing key input
        """
        player = self.gc.player

        #: Safety check: ensure player position exists
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
        if self.gc.player is not None:
            if self.gc.player.health <= 0:
                self.gc.restart_level()
            if self.gc.player.sword_attack:
                for entity in self.gc.entities:
                    if isinstance(entity, Sword):
                        if not entity.ready:
                            entity.apply_cooldown(dt)
                        if entity.ready:
                            self.gc.entities.remove(entity)
                            self.gc.player.sword_attack = False


    def sword_attack(self):
            self.gc.player.sword_attack = True
            self.gc.create_entity("sword",
                                  x=self.gc.player.face_direction[0]
                                    + self.gc.player.x,
                                  y= self.gc.player.face_direction[1]
                                    + self.gc.player.y)
            swords = [entity for entity in self.gc.entities if "SW" in entity.id]
            for sword in swords:
                self.gc.cc.check_entity_collision(sword.x, sword.y, sword)