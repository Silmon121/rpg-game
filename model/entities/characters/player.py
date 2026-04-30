"""
Player module.

Define the Player class, which represents the main controllable
character in the game.
"""

from model.entities.characters.character import Character


class Player(Character):
    """
    Represent the player-controlled character.

    Extend Character with player-specific attributes and behavior,
    such as combat state and increased base health.
    """

    #: Unique prefix for player entities.
    __ID_PREFIX = "P"

    #: Expected parameters for Player initialization.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    __WANTED_FIELDS: list[str] = []

    #: Player maximum health.
    _max_health = 100

    def __init__(self, **kwargs):
        """
        Initialize Player instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Character constructor.
        """
        super().__init__(**kwargs)
        self.sword_attack = False

    def __str__(self) -> str:
        """
        Return a human-readable string representation.

        Returns
        -------
        str
            Player summary including name and health.
        """
        return f"Player\nName: {self._name}\nHP: {self._hp}\n"

    def __init_subclass__(cls):
        """
        Initialize Player subclass.

        Ensure inheritance chain initialization rules are preserved.
        """
        super().__init_subclass__()
