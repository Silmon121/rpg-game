from .entity import Entity
from abc import ABC
import registry as reg

class MovableEntity(Entity, ABC):
    __ID_PREFIX = "ME"
    __EXPECTED_PARAMETERS: dict[str, type] = {

    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.cc =

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        #bounds
        if reg.game.cc.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y