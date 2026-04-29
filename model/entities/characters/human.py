"""Human character module"""
from .npc import NPC


class Human(NPC):
    #: Unique prefix for NPC entities.
    __ID_PREFIX = "HU"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
    }

    #: Light Elf max health
    _max_health = 100

    #: Light Elf dmg
    _damage: int = 20

    #: Time limit for entity to move
    _time_to_move = 2.3

    #: Probability to move
    _prob_to_move = 0.75
    """Human character class"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)