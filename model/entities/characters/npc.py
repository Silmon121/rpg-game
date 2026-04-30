"""
NPC (Non-Player Character) module.

Define AI-controlled characters in the game world.
"""

import random
from .character import Character


class NPC(Character):
    """
    Represent a non-player character controlled by game logic.

    Extend Character with basic AI movement behavior and
    optional aggressive (agro) combat behavior.
    """

    #: Unique prefix for NPC entities.
    __ID_PREFIX = "NPC"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "agro": bool
    }

    #: Time interval between movement decisions.
    _time_to_move = 5

    #: Probability of performing a movement action.
    _prob_to_move = 0.8

    def __init__(self, **kwargs):
        """
        Initialize NPC instance.

        Parameters
        ----------
        agro : bool, optional
            Determines whether NPC is aggressive toward targets.
        """
        super().__init__(**kwargs)

        self.move_timer = 0.0
        self._agro = kwargs.get("agro", True)

    def update_position(self, dt):
        """
        Update NPC movement based on internal timing and randomness.

        Parameters
        ----------
        dt : float
            Time delta since last update.
        """
        self.move_timer += dt

        if self.move_timer >= self._time_to_move:
            if random.random() < self._prob_to_move:
                axis = random.randint(0, 1)

                if axis == 0:
                    dx = -1 if random.randint(0, 1) == 0 else 1
                    self.move(dx, 0)
                else:
                    dy = -1 if random.randint(0, 1) == 0 else 1
                    self.move(0, dy)

            self.move_timer = 0.0

    def attack(self, target):
        """
        Perform an attack on a target if NPC is aggressive.

        Parameters
        ----------
        target : Character
            Entity receiving damage.
        """
        if self._agro:
            target.health -= self._damage

    # =========================================================
    # Properties
    # =========================================================

    @property
    def agro(self) -> bool:
        """
        Return whether NPC is aggressive.

        Returns
        -------
        bool
            True if NPC can initiate attacks.
        """
        return self._agro
