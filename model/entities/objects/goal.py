"""
Goal entity module.

Represent a goal tile that marks level completion.
"""

from model.entities.entity import Entity


class Goal(Entity):
    """
    Represent a goal tile.

    Used as an objective tile in the game world. Reaching this
    tile typically triggers level completion.
    """

    #: Unique prefix for Floor entities.
    __ID_PREFIX: str = "G"

    #: Floor has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize Goal instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
