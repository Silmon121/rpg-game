"""Light elf npc class module"""

from model.entities.characters.npc import NPC

class LightElf(NPC):
    """Light elf npc class"""

    #: Unique prefix for NPC entities.
    __ID_PREFIX = "LE"

    #: Expected initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {
    }

    #: Light Elf max health
    _max_health = 80

    #: Light Elf dmg
    _damage: int = 10

    #: Time limit for entity to move
    _time_to_move = 3

    #: Probability to move
    _prob_to_move = 0.75

    def __init__(self, **kwargs):
        """
        Initialize an NPC entity.

        Args:

        """
        super().__init__(**kwargs)

