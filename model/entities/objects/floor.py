"""
Floor entity module.

Represent a non-blocking ground tile in the game world.
"""

from model.entities.entity import Entity


class Floor(Entity):
    """
    Represent a walkable terrain tile.

    Extend the base Entity with no additional behavior.
    Used as a non-interactive ground element in the map grid.
    """

    #: Unique prefix for Floor entities.
    __ID_PREFIX: str = "F"

    #: Floor has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize Floor instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
