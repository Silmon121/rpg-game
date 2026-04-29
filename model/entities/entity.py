"""
Entity module.

The base module for all other entity based modules.
"""

from abc import ABC
from typing import Type


class Entity(ABC):
    """
    Base abstract class for all game entities.

    Provides:
    - Unique ID generation with class hierarchy prefixes
    - Position handling (x, y)
    - Runtime parameter validation
    - Inheritance enforcement via required class fields

    This class is intended to be subclassed, not used directly.
    """

    #: Unique prefix for "Entity" class.
    __ID_PREFIX: str = "E"

    #: Unique set of parameters for "Entity" init.
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "x": int,
        "y": int,
        "name": str
    }

    #: Required fields in "Entity" subclasses.
    __WANTED_FIELDS: list[str] = ["__ID_PREFIX", "__EXPECTED_PARAMETERS"]

    #: ID counter for the amount of instances created.
    _id_counter: int = 0

    def __init__(self, **kwargs):
        """
        Initialize an entity with validated parameters.

        Expected kwargs:
            x (int, optional): X position (must be >= 0)
            y (int, optional): Y position (must be >= 0)
            name (str, optional): Entity name

        Raises:
            ValueError: If invalid parameters
            or negative coordinates are provided
        """
        # Validate parameters against expected schema
        self._expected_parameters = (
            self.__load_parameters())
        self.__check_parameters(given=kwargs,
                                expected=self._expected_parameters)

        # Extract values
        x = kwargs.get("x", None)
        y = kwargs.get("y", None)
        name = kwargs.get("name", None)

        # Validate coordinates
        if x is not None and x < 0:
            raise ValueError("x must be positive")
        if y is not None and y < 0:
            raise ValueError("y must be positive")

        # Initialization
        self._id = self.__generate_id(self.__get_prefix_chain())
        self._code = self.__class__.__name__.title()
        self._name = name or self._code

        self._position = (
            [x, y]
            if x is not None and y is not None and x >= 0 and y >= 0
            else [None, None]
        )

    def __str__(self):
        """Return string representation of the entity."""
        pass

    def __repr__(self):
        """
        Return developer-friendly representation of the entity.

        Includes ID, code, name, and position.
        """
        return (
            f"ENTITY INFO:\n"
            f"ID: {self._id}\n"
            f"Code: {self._code}\n"
            f"Name: {self._name}\n"
            f"X: {self.x}\n"
            f"Y: {self.y}"
        )

    def __init_subclass__(cls):
        """
        Enforce required class-level fields in subclasses.

        Each subclass must define:
            - __ID_PREFIX
            - __EXPECTED_PARAMETERS
        """
        super().__init_subclass__()

        for field in cls.__WANTED_FIELDS:
            mangled_field = f"_{cls.__name__}{field}"
            if mangled_field not in cls.__dict__.keys():
                raise TypeError(
                    f"Class '{cls.__name__}' is missing "
                    f"required field: {field}"
                )

    # =========================================================
    # Properties
    # =========================================================

    @property
    def id(self) -> str:
        """Unique entity ID."""
        return self._id

    @property
    def name(self) -> str:
        """Entity name."""
        return self._name

    @property
    def position(self) -> list:
        """
        Entity position as [x, y].

        Raises:
            ValueError: If position is not fully initialized.
        """
        for item in self._position:
            if item is None:
                raise ValueError(
                    f"Position is missing for entity "
                    f"{self._id} : {self._code} : {self._name}"
                )
        return self._position

    @property
    def x(self) -> int:
        """X coordinate."""
        return self._position[0]

    @property
    def y(self) -> int:
        """Y coordinate."""
        return self._position[1]

    # =========================================================
    # Setters
    # =========================================================

    @name.setter
    def name(self, value: str):
        """Set entity name."""
        self._name = value

    @x.setter
    def x(self, value: int):
        """Set X coordinate (must be >= 0)."""
        if value < 0:
            raise ValueError("x must be positive")
        self._position[0] = value

    @y.setter
    def y(self, value: int):
        """Set Y coordinate (must be >= 0)."""
        if value < 0:
            raise ValueError("y must be positive")
        self._position[1] = value

    # =========================================================
    # Class methods
    # =========================================================

    @classmethod
    def __generate_id(cls: Type["Entity"], prefixes: list[str]) -> str:
        """
        Generate a unique entity ID.

        Format:
            PREFIX-PREFIX-00001

        Args:
            prefixes (list[str]): Hierarchy-based prefix chain

        Returns:
            str: Generated unique ID
        """
        return "-".join(prefixes) + "-" + f"{cls.__next_id():05}"

    @classmethod
    def __get_prefix_chain(cls: Type["Entity"]) -> list[str]:
        """
        Build inheritance-based prefix chain from class hierarchy.

        Returns:
            list[str]: Ordered list of ID prefixes
        """
        return [
            getattr(base, f"_{base.__name__}__ID_PREFIX")
            for base in reversed(cls.__mro__)
            if hasattr(base, f"_{base.__name__}__ID_PREFIX")
        ]

    @classmethod
    def __next_id(cls: Type["Entity"]) -> int:
        """
        Increment and return the class-wide ID counter.

        Returns:
            int: Next ID value
        """
        if not hasattr(cls, "_id_counter"):
            raise TypeError(f"Class {cls.__name__} lacks an id counter")

        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def __load_parameters(cls) -> dict[str, type]:
        """
        Load and merge expected parameters from class hierarchy.

        Returns:
            dict[str, type]: Combined parameter schema
        """
        wanted_field = "__EXPECTED_PARAMETERS"
        complete_dict = {}

        for base in reversed(cls.__mro__):
            mangled = f"_{base.__name__}{wanted_field}"
            if hasattr(base, mangled):
                complete_dict.update(getattr(base, mangled))

        return complete_dict

    # =========================================================
    # Validation helpers
    # =========================================================

    @staticmethod
    def __check_parameters(given: dict[str, type], expected: dict[str, type]):
        """
        Validate provided parameters against expected schema.

        Args:
            given (dict): Provided arguments
            expected (dict): Expected parameter types

        Raises:
            ValueError: If unknown or invalid parameter types are found
        """
        for key in given:
            if key not in expected:
                raise ValueError(
                    f"Invalid parameter '{key}'. "
                    f"Allowed: {list(expected.keys())}"
                )

        for key, value in given.items():
            if not isinstance(value, expected[key]):
                raise ValueError(
                    f"Invalid type for '{key}': "
                    f"got {type(value).__name__}, "
                    f"expected {expected[key].__name__}"
                )
