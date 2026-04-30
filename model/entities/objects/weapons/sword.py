"""
Sword entity module.

Represent a melee weapon entity used in the game world.
"""

from model.entities.objects.weapons.weapon import Weapon


class Sword(Weapon):
    """
    Represent a sword weapon.

    Extend the Weapon base class with no additional behavior.
    Used as a melee weapon entity within the game.
    """

    #: Unique prefix for movable entities.
    __ID_PREFIX = "SW"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize Sword instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Weapon constructor.
        """
        super().__init__(**kwargs)
