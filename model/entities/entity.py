from abc import ABC, abstractmethod
from typing import Type

from IPython.core.interactiveshell import is_integer_string


class Entity(ABC):
    __ID_PREFIX: str = "E"
    __id_counter: int = 0

    @staticmethod
    def _check_parameters(given_params: dict [str, type], expected_parameters: dict[str, type]):
        additional_parameters = set(given_params.keys()) - set(expected_parameters.keys())
        if additional_parameters:
            raise ValueError(f"Invalid parameters: {additional_parameters}\nPlease use valid parameters: {expected_parameters.keys()}")

        for key, value in given_params.items():
            if not isinstance(value, expected_parameters[key]):
                raise ValueError(f"Value for parameter {key} is {value}, expected {expected_parameters[key]}")

    def __init__(self, **kwargs):
        expected_parameters = {"x": int, "y": int, "name": str}
        self._check_parameters()

        # Assignment
        x = kwargs.pop("x", None) if isinstance(kwargs["x"], int) else None
        y = kwargs.pop("y", None) if isinstance(kwargs["y"], int) else None
        name = kwargs.pop("name", None) if isinstance(kwargs["name"], str) else None

        # Initialization
        self._id = self.__generate_id(self.__get_prefix_chain())
        self._code = self.__class__.__name__.title()
        self._name = name or self._code
        self.__position = [x, y] if (x is not None and y is not None) and (x >= 0 and y >= 0) else [None, None]

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return f"ENTITY INFO:\nID: {self._id}\nCode: {self._code}\nName: {self._name}\nX: {self.x}\nY: {self.y}"


    # Getters
    @property
    def name(self) -> str:
        return self._name
    @property
    def position(self) -> list:
        for item in self.__position:
            if item is None:
                raise ValueError(f"Position is missing for entity {self._id} : {self._code} : {self._name}")
        return self.__position
    @property
    def x(self) -> int:
        return self.__position[0]
    @property
    def y(self) -> int:
        return self.__position[1]


    # Setters
    @name.setter
    def name(self, value: str):
        self._name = value

    @x.setter
    def x(self, value: int):
        if value < 0:
            raise ValueError("x must be positive")
        self.__position[0] = value

    @y.setter
    def y(self, value: int):
        if value < 0:
            raise ValueError("y must be positive")
        self.__position[1] = value


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
        return "-".join(prefixes) + "_" + str(cls.__next_id())


    @classmethod
    def __get_prefix_chain(cls: Type["Entity"]) -> list[str]:
        """
        Returns hierarchy chain of a child to the highest parent.

        :return: List of prefixes
        :rtype: list[str]
        """
        return [getattr(base, f"_{base.__name__}__ID_PREFIX") for base in reversed(cls.__mro__) if hasattr(base, f"_{base.__name__}__ID_PREFIX")]


    @classmethod
    def __next_id(cls: Type["Entity"]) -> int:
        """
        Increase the class _id_counter.

        :param cls: Entity
        :return: incremented id_counter by 1
        :rtype: int
        """
        if not hasattr(cls, f"_{cls.__name__}__id_counter"):
            raise TypeError("This class doesn't have an id counter!")
        cls.__id_counter += 1
        return cls.__id_counter