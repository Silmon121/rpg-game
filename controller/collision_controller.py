from config import *
from model import *
import registry as reg

class CollisionController:
    @staticmethod
    def check_collision(new_x, new_y):
        if not (0 <= new_x < GRID_WIDTH):
            return False
        if not (0 <= new_y < GRID_HEIGHT):
            return False

        for row in reg.game.current_map.grid:
            for cell in row:
                if isinstance(cell, Entity):
                    if isinstance(cell, Wall):
                        if cell.x == new_x and cell.y == new_y:
                            return False
        return True