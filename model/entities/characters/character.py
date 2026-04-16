"""
Character module.

Defines a base class for all living entities in the game,
such as players, NPCs, enemies, etc.
"""

from abc import ABC

from model.entities.movable_entity import MovableEntity


class Character(MovableEntity, ABC):
    """
    Base class for all character-type entities.

    Extends:
        MovableEntity: Adds movement capability
        ABC: Prevents direct instantiation

    Provides:
        - Health system (HP)
        - Combat attributes (strength, intelligence)
        - Immortality flag
    """

    #: Unique prefix for character entities.
    __ID_PREFIX = "CH"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "hp": int,
        "immortal": bool,
        "strength": int,
        "intelligence": int,
    }

    #: Required subclass fields (currently unused).
    __WANTED_FIELDS: list[str] = []

    #: Default maximum health.
    _max_health = 100

    def __init__(self, **kwargs):
        """
        Initialize a character entity.

        Args:
            hp (int, optional): Starting health points.
            immortal (bool): If True, character cannot be killed.
            strength (int): Physical power stat.
            intelligence (int): Mental power stat.
        """
        super().__init__(**kwargs)

        # Extract values
        hp = kwargs.get("hp", None)
        immortal = kwargs.get("immortal", False)
        strength = kwargs.get("strength", 0)
        intelligence = kwargs.get("intelligence", 0)

        # Initialize stats
        self._hp = hp if hp is not None else self._max_health
        self._immortal = immortal
        self._strength = strength
        self._intelligence = intelligence

    def __repr__(self) -> str:
        """Developer-friendly representation of the character."""
        return (
            super().__repr__() +
            f"\nCHARACTER INFO:\n"
            f"Max HP: {self._max_health}\n"
            f"HP: {self._hp}\n"
            f"Immortal: {self._immortal}\n"
        )

    def __init_subclass__(cls):
        """Enforce subclass field requirements."""
        super().__init_subclass__()

        for field in cls.__WANTED_FIELDS:
            if f"_{cls.__name__}{field}" not in cls.__dict__:
                raise TypeError(
                    f"Class '{cls.__name__}' is missing field: {field}"
                )

    # =========================================================
    # Gameplay methods
    # =========================================================

    def attack(self):
        """
        Perform an attack action.

        To be implemented by subclasses.
        """
        pass

    # =========================================================
    # Properties
    # =========================================================

    @property
    def hp(self) -> int:
        """Current health points."""
        return self._hp

    @property
    def is_immortal(self) -> bool:
        """Whether the character is immortal."""
        return self._immortal

    @property
    def strength(self) -> int:
        """Physical strength stat."""
        return self._strength

    @property
    def intelligence(self) -> int:
        """Intelligence stat."""
        return self._intelligence
