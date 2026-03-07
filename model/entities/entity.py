from abc import ABC, abstractmethod
from typing import Type


class Entity(ABC):
    __id_prefix = "E"
    _id_counter = 0

    def __init__(self, name:str= None, x:int= None, y:int= None):
        # ID and naming
        self._id = self.__generate_id(self.__get_prefix_chain())
        self._code = self.__class__.__name__.title()
        if name is None:
            self._name = self._code
        else:
            self._name = name

        # Position
        self._x = x
        self._y = y

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return f"ENTITY INFO:\nID: {self._id}\nCode: {self._code}\nName: {self._name}\nX: {self._x}\nY: {self._y}"


    # Getters
    @property
    def name(self) -> str:
        return self._name
    @property
    def x(self) -> int:
        return self._x
    @property
    def y(self) -> int:
        return self._y


    # Setters
    @name.setter
    def name(self, value: str):
        self._name = value

    @x.setter
    def x(self, value: int):
        if value < 0:
            raise ValueError("x must be positive")
        self._x = value

    @y.setter
    def y(self, value: int):
        if value < 0:
            raise ValueError("y must be positive")
        self._y = value


    # class methods
    @classmethod
    def __generate_id(cls: Type["Entity"], prefixes: list[str]) -> str:
        """
        Generate a unique id for an instance.

        :param prefixes: An id of prefixes to use in the id.
        :type prefixes: list[str]
        :return: New id for instance
        :rtype: str
        """
        return "-".join(prefixes) + "-" + str(cls._next_id())


    @classmethod
    def __get_prefix_chain(cls: Type["Entity"]) -> list[str]:
        """
        Returns hierarchy chain of a child to the highest parent.

        :return: List of prefixes
        :rtype: list[str]
        """
        return [getattr(base, f"_{base.__name__}__id_prefix") for base in reversed(cls.__mro__) if hasattr(base, f"_{base.__name__}__id_prefix")]


    @classmethod
    def __next_id(cls: Type["Entity"]) -> int:
        """
        Increase the class _id_counter.

        :param cls: Entity
        :return: incremented id_counter by 1
        :rtype: int
        """
        if not hasattr(cls, "_id_counter"):
            pass
        cls._id_counter += 1
        return cls._id_counter