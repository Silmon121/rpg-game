"""
Light elf NPC module.

Define the LightElf class, representing a fast, lightly
armored NPC with higher mobility and lower health.
"""

from model.entities.characters.npc import NPC


class LightElf(NPC):
    """
    Represent a Light Elf NPC entity.

    Extend NPC with lightweight combat stats and increased
    movement frequency.
    """

    #: Unique prefix for Light Elf NPC entities.
    __ID_PREFIX = "LE"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: Default maximum health value.
    _max_health = 80

    #: Default damage value.
    _damage: int = 15

    #: Time interval between movement decisions.
    _time_to_move = 2.5

    #: Probability of performing a movement action.
    _prob_to_move = 0.75

    def __init__(self, **kwargs):
        """
        Initialize LightElf NPC instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to NPC constructor.
        """
        super().__init__(**kwargs)
