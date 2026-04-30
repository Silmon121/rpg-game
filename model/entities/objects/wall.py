"""
Wall entity module.

Represent an impassable obstacle in the game world.
"""

from model.entities.entity import Entity


class Wall(Entity):
    """
    Represent an impassable world object.

    Used as a blocking element in the map grid. Prevents movement
    of players and other entities through its position.
    """

    #: Unique prefix for Wall entities.
    __ID_PREFIX: str = "W"

    #: Wall has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: Visual color representation (RGB).
    __COLOR = (0, 255, 0)

    def __init__(self, **kwargs):
        """
        Initialize Wall instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
