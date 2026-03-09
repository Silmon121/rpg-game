from model import Entity
from abc import ABC, abstractmethod

class Character(Entity, ABC):
    __ID_PREFIX = "CH"
    _max_health = 100

    def __init__(self, **kwargs):
        parameters = {"hp", "immortal"}
        if parameters in kwargs.keys():
            hp = kwargs.pop("hp", self._max_health)
        super().__init__(kwargs)
        self._hp = hp if hp is not None else self._max_health
        self._immortal = immortal


    def __repr__(self):
        return super().__repr__() + f"\nCHARACTER INFO:\nMax HP: {self._max_health}\nHP: {self._hp}\nImmortal: {self._immortal}\n"


    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def attack(self):
        pass


    @property
    def hp(self):
        return self._hp

    @property
    def mortal(self):
        return self._immortal