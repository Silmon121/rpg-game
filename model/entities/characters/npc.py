from model import Entity
from abc import ABC, abstractmethod

class NPC(Entity, ABC):
    _id_prefix = "NPC"
    def __init__(self,name=_id_prefix):
        super().__init__(name)

    @abstractmethod
    def move(self):
        pass
    def attack(self):
        pass