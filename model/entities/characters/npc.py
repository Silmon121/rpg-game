"""
NPC (Non-Player Character) module.

Defines AI-controlled characters in the game world.
"""

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

    def __init__(self, **kwargs):
        """
        Initialize an NPC entity.

        Args:
            agro (bool, optional): Whether NPC is aggressive.
        """
        super().__init__(**kwargs)

        self._agro = kwargs.get("agro", False)

    # =========================================================
    # Properties
    # =========================================================

    @property
    def agro(self) -> bool:
        """Whether the NPC is aggressive toward the player."""
        return self._agro
