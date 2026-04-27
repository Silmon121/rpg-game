"""
NPC (Non-Player Character) module.

Defines AI-controlled characters in the game world.
"""

import random
from .character import Character


class NPC(Character):
    """
    Non-player character controlled by game logic or AI.

    Extends:
        Character: Base stats + movement + combat

    Adds:
        - Aggro behavior flag (agro)
    """

    #: Unique prefix for NPC entities.
    __ID_PREFIX = "NPC"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "agro": bool
    }

    #: Time to move for an npc
    _time_to_move = 5

    #: Probability to move
    _prob_to_move = 0.8

    def __init__(self, **kwargs):
        """
        Initialize an NPC entity.

        Args:
            agro (bool, optional): Whether NPC is aggressive.
        """
        super().__init__(**kwargs)
        self.move_timer = 0.0
        self._agro = kwargs.get("agro", True)

    def update_position(self, dt):
        self.move_timer += dt

        if self.move_timer >= self._time_to_move:
            if random.random() < self._prob_to_move:
                dx = random.randint(0, 1)
                dy = random.randint(0, 1)

                dx = -1 if dx == 0 else 1
                dy = -1 if dy == 0 else 1

                self.move(dx,dy)

            self.move_timer = 0.0

    # =========================================================
    # Properties
    # =========================================================

    @property
    def agro(self) -> bool:
        """Whether the NPC is aggressive toward the player."""
        return self._agro
