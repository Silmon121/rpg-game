"""
Wall entity module.

Represents an impassable obstacle in the game world.
Walls block movement and are used for map boundaries and structures.
"""

from model.entities.entity import Entity


class Wall(Entity):
    """
    Impassable world object.

    Extends:
        Entity: Base entity system (ID, position, validation)

    Purpose:
        Prevents player and NPC movement through its position.
    """

    #: Unique prefix for Wall entities.
    __ID_PREFIX: str = "W"

    #: Wall has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: Visual color representation (RGB).
    __COLOR = (0, 255, 0)

    def __init__(self, **kwargs):
        """
        Initialize a Wall tile.

        Args:
            **kwargs: Passed to base Entity constructor.
        """
        super().__init__(**kwargs)
