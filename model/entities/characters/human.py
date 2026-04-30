"""
Human character module.

Define the Human NPC class, which represents a human-type
non-player character in the game world.
"""

from .npc import NPC


class Human(NPC):
    """
    Represent a human NPC character.

    Extend NPC with human-specific behavior parameters such as
    movement probability and timing constraints.
    """

    #: Unique prefix for human NPC entities.
    __ID_PREFIX = "HU"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: Default maximum health value.
    _max_health = 100

    #: Default damage value.
    _damage: int = 20

    #: Time interval between movement decisions.
    _time_to_move = 2.3

    #: Probability of performing a movement action.
    _prob_to_move = 0.75

    def __init__(self, **kwargs):
        """
        Initialize Human NPC instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to NPC constructor.
        """
        super().__init__(**kwargs)
