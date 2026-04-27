"""
Movable entity module.

Provides an abstract base class for all entities
that can move within the game world.
"""

from abc import ABC
from .entity import Entity
import registry as reg


class MovableEntity(Entity, ABC):
    """
    Abstract base class for entities that support movement.

    Extends:
        Entity: Base entity functionality
        ABC: Prevents direct instantiation

    Provides:
        - Movement logic (dx, dy)
        - Collision-aware position updates
    """

    #: Unique prefix for movable entities.
    __ID_PREFIX = "ME"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize a movable entity.

        Args:
            **kwargs: Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
        self.face_direction = (1,0)

    def move(self, dx: int, dy: int):
        """
        Move the entity by a delta (dx, dy) if no collision occurs.

        Args:
            dx (int): Change in x direction.
            dy (int): Change in y direction.

        Notes:
            Movement is blocked if collision is detected.
        """

        if dx == -1:
            self.face_direction = (-1,0)
        elif dx == 1:
            self.face_direction = (1, 0)
        elif dy == -1:
            self.face_direction = (0, -1)
        elif dy == 1:
            self.face_direction = (0, 1)

        new_x = self.x + dx
        new_y = self.y + dy

        # Collision check
        if reg.game.cc.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
        reg.game.cc.check_entity_collision(new_x, new_y, self)