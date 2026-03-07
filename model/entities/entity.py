from abc import ABC, abstractmethod
from typing import Type


class Entity(ABC):
    _id_prefix = "E"

    def __init__(self, name:str= None):
        """
        The main constructor for entities.

        :param name: Name of the instance
        :type name: str
        """
        self._id = self._generate_id(self._get_prefix_chain())
        self._code = self.__class__.__name__.lower()
        if name is None:
            self._name = self.__class__.__name__.title()
        else:
            self._name = name

    def __str__(self):
        return f"{self._name}"

    def __repr__(self):
        return f"{self._code}: {self._name}: {self.name}"

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def name(self) -> str:
        return self._name


    # class methods
    @classmethod
    def _generate_id(cls, prefixes: list[str]) -> str:
        """
        Generate a unique id for an instance.

        :param prefixes: An id of prefixes to use in the id.
        :type prefixes: list[str]
        :return: New id for instance
        :rtype: str
        """
        return "-".join(prefixes) + f"-{cls._id_prefix}-" + str(cls._next_id())


    @classmethod
    def _get_prefix_chain(cls: Type["Entity"]) -> list[str]:
        """
        Returns

        :return: List of prefixes
        :rtype: list[str]
        """
        return [getattr(base, "_id_prefix") for base in reversed(cls.__mro__) if hasattr(base, "_id_prefix")]


    @classmethod
    def _next_id(cls: Type["Entity"]) -> int:
        """
        Creates id counter in each subclass if it hasn't been created already.
        Main purpose is to increase the value of id_counter for new id entries.
        :param cls: Entity
        :return: incremented id_counter by 1
        :rtype: int
        """
        if not hasattr(cls, "__id_counter"):
            cls._id_counter = 0
        cls._id_counter += 1
        return cls._id_counter
