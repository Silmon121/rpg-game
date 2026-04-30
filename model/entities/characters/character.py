"""
Character module.

Define a base class for all living entities in the game,
such as players, NPCs, and enemies.
"""

from abc import ABC
from model.entities.movable_entity import MovableEntity


class Character(MovableEntity, ABC):
    """
    Represent a base class for all character-type entities.

    Extend MovableEntity with health, combat stats, and
    immortality support.
    """

    #: Unique prefix for character entities.
    __ID_PREFIX = "CH"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "hp": int,
        "immortal": bool,
    }

    #: Default maximum health.
    _max_health = 100

    #: Default damage.
    _damage = 20

    def __init__(self, **kwargs):
        """
        Initialize Character instance.

        Parameters
        ----------
        hp : int, optional
            Starting health points. If not provided,
            the maximum health value is used.
        immortal : bool, optional
            If set to True, the character cannot be killed.
        """
        super().__init__(**kwargs)

        # Extract values
        hp = kwargs.get("hp", None)
        immortal = kwargs.get("immortal", False)

        # Initialize stats
        self._hp = hp if hp is not None else self._max_health
        self._immortal = immortal

    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.

        Returns
        -------
        str
            Detailed character state including health and flags.
        """
        return (
                super().__repr__() +
                "\nCHARACTER INFO:\n"
                f"Max HP: {self._max_health}\n"
                f"HP: {self._hp}\n"
                f"Immortal: {self._immortal}\n"
        )

    def __init_subclass__(cls):
        """Subclass initialization hook."""
        super().__init_subclass__()

    # =========================================================
    # Gameplay methods
    # =========================================================

    def attack(self, target):
        """
        Apply damage to a target entity.

        Parameters
        ----------
        target : Character
            Entity receiving damage.
        """
        target.health -= self._damage

    def take_damage(self, attacker):
        """
        Reduce health based on incoming attacker damage.

        Parameters
        ----------
        attacker : Character
            Entity dealing damage.
        """
        self._hp -= attacker.damage

    # =========================================================
    # Properties
    # =========================================================

    @property
    def health(self) -> int:
        """
        Return current health value.

        Returns
        -------
        int
            Current HP.
        """
        return self._hp

    @property
    def is_immortal(self) -> bool:
        """Return whether character is immortal."""
        return self._immortal

    @property
    def damage(self) -> int:
        """Return character damage value."""
        return self._damage

    @property
    def max_health(self) -> int:
        """Return maximum health value."""
        return self._max_health

    @health.setter
    def health(self, value):
        """Set current health value."""
        self._hp = value
