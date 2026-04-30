"""
Orc NPC module.

Define the Orc class, representing a strong, high-health
NPC with increased damage and slower movement behavior.
"""

from .npc import NPC


class Orc(NPC):
    """
    Represent an Orc NPC entity.

    Extend NPC with high durability and increased combat
    strength at the cost of slower movement behavior.
    """

    #: Unique prefix for Orc NPC entities.
    __ID_PREFIX = "OR"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: Default maximum health value.
    _max_health = 120

    #: Default damage value.
    _damage: int = 25

    #: Time interval between movement decisions.
    _time_to_move = 2

    #: Probability of performing a movement action.
    _prob_to_move = 0.8

    def __init__(self, **kwargs):
        """
        Initialize Orc NPC instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to NPC constructor.
        """
        super().__init__(**kwargs)
