"""
Collision system module.

Provides logic for validating movement and detecting
collisions with world boundaries and entities.
"""

from config import GRID_HEIGHT, GRID_WIDTH
from model import Wall, Goal, NPC, Player, Weapon

class CollisionController:
    """
    Handles collision detection for the game world.

    Responsibilities:
        - Prevent movement outside map bounds
        - Detect collisions with solid entities (e.g., walls)
    """

    def __init__(self, game_controller):
        self.gc = game_controller

    def check_collision(self, new_x: int, new_y: int, call_entity) -> bool:
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
        for row in self.gc.current_map.grid:
            for cell in row:
                if cell.x == new_x and cell.y == new_y:
                    if isinstance(cell, Wall):
                        return False
                    elif isinstance(cell, Goal):
                        if self.gc.level_cleared:
                            self.gc.next_level()
                        else:
                            return False
        if not self.__check_entity_collision(new_x, new_y, call_entity):
            return False
        return True

    def __check_entity_collision(self, new_x: int, new_y: int, call_entity) -> bool:
        for entity in self.gc.entities:
            if entity.id != call_entity.id:
                if entity.x == new_x and entity.y == new_y:
                    if isinstance(call_entity, Player):
                        if isinstance(entity, NPC):
                            call_entity.take_damage(entity)
                    elif isinstance(call_entity, NPC):
                        if isinstance(entity, Player):
                            call_entity.attack(entity)
                        elif isinstance(call_entity, NPC):
                            return False
                    if isinstance(call_entity, Weapon):
                        if isinstance(entity, NPC):
                            self.gc.player.attack(entity)
        return True
