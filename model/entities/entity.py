from abc import ABC, abstractmethod


class Entity(ABC):
    __id = None
    __code = "entity"
    __name = "Entity"

    _id_counter = 1

    _max_hp = 100

    def __init__(self, name):
        self.__hp = self._max_hp
        self.__id = self._generate_id()

    def __str__(self):
        return f"{self._name}"
    def __repr__(self):
        return f"{self._name}: {self._id}"

    @property
    @abstractmethod
    def name(self):
        return self._name

    @name.setter
    @abstractmethod
    def name(self,value):
        raise ValueError("Name can't be changed")

    def _generate_id(self, template):

        return Entity._id_counter
