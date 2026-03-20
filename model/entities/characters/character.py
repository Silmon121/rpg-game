from model.entities.movable_entity import MovableEntity
from abc import ABC

class Character(MovableEntity, ABC):
    __ID_PREFIX = "CH"
    __EXPECTED_PARAMETERS: dict[str, type] = {
        "hp": int,
        "immortal": bool,
        "strength": int,
        "intelligence": int,
    }
    __WANTED_FIELDS: list[str] = []
    _max_health = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Declaration
        hp = kwargs.get("hp", None)
        immortal = kwargs.get("immortal", False)
        strength = kwargs.get("strength", 0)
        intelligence = kwargs.get("intelligence", 0)


        # Initialization
        self._hp = hp if hp is not None else self._max_health
        self._immortal = immortal

        # abilities
        self._strength = strength
        self._intelligence = intelligence


    def __repr__(self):
        return super().__repr__() + f"\nCHARACTER INFO:\nMax HP: {self._max_health}\nHP: {self._hp}\nImmortal: {self._immortal}\n"

    def __init_subclass__(cls):
        super().__init_subclass__()
        for field in cls.__WANTED_FIELDS:
            if f"_{cls.__name__}{field}" not in cls.__dict__:
                raise TypeError(f"This class '{cls.__name__}' doesn't have {field} field!")

    def attack(self):
        pass

    @property
    def hp(self):
        return self._hp
    @property
    def mortal(self):
        return self._immortal
    @property
    def strength(self):
        return self._strength
    @property
    def intelligence(self):
        return self._intelligence