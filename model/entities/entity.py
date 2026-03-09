from abc import ABC, abstractmethod
from typing import Type


class Entity(ABC):
    __ID_PREFIX: str = "E"
    __expected_parameters: dict[str, type] = {
        "x": int,
        "y": int,
        "name": str
    }
    _id_counter: int = 0

    def __init__(self, **kwargs):
        self.__expected_parameters = self.__load_parameters() # creating an instance copy of the __expected_parameters on a class level
        self._check_parameters(given=kwargs, expected=self.__expected_parameters)
        # Assignment
        x = kwargs.get("x", None)
        if x is not None:
            if x < 0:
                raise ValueError("x must be positive")
        y = kwargs.get("y", None)
        if y is not None:
            if y < 0:
                raise ValueError("y must be positive")
        name = kwargs.get("name", None)

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

    def __init_subclass__(cls):
        super.__init_subclass__()
        wanted_fields = {"__ID_PREFIX", "__expected_parameters"}
        for field in wanted_fields:
            if f"_{cls.__name__}{field}" not in cls.__dict__.keys():
                raise TypeError(f"This class {cls.__name__} doesn't have {field} field!")
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
        return "-".join(prefixes) + "-" + f"{cls.__next_id():05}"


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
        wanted_field = f"_id_counter"
        if not hasattr(cls, wanted_field):
            raise TypeError(f"This class {cls.__name__} doesn't have an id counter!")
        cls._id_counter += 1
        return cls._id_counter


    @classmethod
    def __load_parameters(cls) -> dict[str, type]:
        wanted_field = "__expected_parameters"
        complete_dict = {}
        for base in reversed(cls.__mro__):
            if hasattr(base, f"_{base.__name__}{wanted_field}"):
                complete_dict.update(getattr(base, f"_{base.__name__}{wanted_field}"))
        return complete_dict


    @staticmethod
    def _check_parameters(given: dict[str, type], expected: dict[str, type]):
        for key in given:
            if key not in expected:
                raise ValueError(f"Invalid parameter '{key}'\nPlease use valid parameters: {expected.keys()}")

        for key, value in given.items():
            if not isinstance(value, expected[key]):
                raise ValueError(f"Value for parameter {key} is {value}, expected {expected[key]}")