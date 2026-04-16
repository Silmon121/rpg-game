"""
Collision system module.

Provides logic for validating movement and detecting
collisions with world boundaries and entities.
"""

from config import GRID_HEIGHT, GRID_WIDTH
from model import Wall
import registry as reg


class CollisionController:
    """
    Handles collision detection for the game world.

    Responsibilities:
        - Prevent movement outside map bounds
        - Detect collisions with solid entities (e.g., walls)
    """

    @staticmethod
    def check_collision(new_x: int, new_y: int) -> bool:
        """
        Check whether a position is valid (no collision).

        Args:
            new_x (int): Target X coordinate.
            new_y (int): Target Y coordinate.

        Returns:
            bool:
                True if movement is allowed,
                False if collision occurs.
        """
        # Boundary check
        if not (0 <= new_x < GRID_WIDTH):
            return False
        if not (0 <= new_y < GRID_HEIGHT):
            return False

        # Entity collision check
        for row in reg.game.current_map.grid:
            for cell in row:
                if isinstance(cell, Wall):
                    if cell.x == new_x and cell.y == new_y:
                        return False

        return True
