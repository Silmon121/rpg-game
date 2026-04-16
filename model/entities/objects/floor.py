"""
Floor entity module.

Represents a non-blocking ground tile in the game world.
Floors are walkable and serve as base terrain.
"""

from model.entities.entity import Entity


class Floor(Entity):
    """
    Walkable terrain tile.

    Extends:
        Entity: Base entity system (ID, position, validation)

    Purpose:
        Acts as a non-interactive ground element in the map grid.
    """

    #: Unique prefix for Floor entities.
    __ID_PREFIX: str = "F"

    #: Floor has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize a Floor tile.

        Args:
            **kwargs: Passed to base Entity constructor.
        """
        super().__init__(**kwargs)
