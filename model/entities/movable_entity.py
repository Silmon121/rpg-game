"""
Movable entity module.

Provide an abstract base class for all entities that can move
within the game world.
"""

from abc import ABC
from .entity import Entity
import registry as reg
from config import Direction


class MovableEntity(Entity, ABC):
    """
    Represent an entity that supports movement.

    Extends the base Entity with movement behavior and
    collision-aware position updates.
    """

    #: Unique prefix for movable entities.
    __ID_PREFIX = "ME"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize MovableEntity instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
        self.face_direction = Direction.RIGHT

    def __init_subclass__(cls):
        """Continue the validation chain."""
        super().__init_subclass__()

    def move(self, dx: int, dy: int):
        """
        Move entity by a delta (dx, dy).

        Update the entity position if no collision is detected.

        Parameters
        ----------
        dx : int
            Change in horizontal direction.
        dy : int
            Change in vertical direction.
        """
        if dx == -1:
            self.face_direction = Direction.LEFT
        elif dx == 1:
            self.face_direction = Direction.RIGHT
        elif dy == -1:
            self.face_direction = Direction.UP
        elif dy == 1:
            self.face_direction = Direction.DOWN

        new_x = self.x + dx
        new_y = self.y + dy

        # Collision check
        if reg.game.cc.check_collision(new_x, new_y, self):
            self.x = new_x
            self.y = new_y
