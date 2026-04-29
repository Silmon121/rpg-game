"""Sword class module"""
from model.entities.objects.weapons.weapon import Weapon


class Sword(Weapon):
    #: Unique prefix for movable entities.
    __ID_PREFIX = "SW"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """Initialize the Sword class."""
        super().__init__(**kwargs)
