"""Orc character model"""

from .npc import NPC

class Orc(NPC):
    """Orc character model"""
    #: Unique prefix for NPC entities.
    __ID_PREFIX = "OR"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {

    }

    #: Orc max health
    _max_health = 120

    #: Orc dmg
    _damage: int = 25

    #: Time limit for entity to move
    _time_to_move = 2

    #: Probability to move
    _prob_to_move = 0.8

    def __init__(self, **kwargs):
        """Orc constructor"""
        super().__init__(**kwargs)
