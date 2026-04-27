"""
Player module.

Defines the Player class, which is the main controllable
character in the game.
"""

from model.entities.characters.character import Character


class Player(Character):
    """
    Player-controlled character.

    Extends:
        Character: Base character logic (stats, movement, combat)

    Customizations:
        - Higher base health
        - Player-specific string representation
    """

    #: Unique prefix for player entities.
    __ID_PREFIX = "P"

    #: Expected parameters for Player initialization.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    __WANTED_FIELDS: list[str] = []

    #: Player-specific maximum health.
    _max_health = 120

    def __init__(self, **kwargs):
        """Initialize a Player instance."""
        super().__init__(**kwargs)
        self.sword_attack = False

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"Player\nName: {self._name}\nHP: {self._hp}\n"

    def __init_subclass__(cls):
        """Ensure subclass validation rules are enforced."""
        super().__init_subclass__()
