"""Goal class module"""

from model.entities.entity import Entity

class Goal(Entity):
    #: Unique prefix for Floor entities.
    __ID_PREFIX: str = "G"

    #: Floor has no additional initialization parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    def __init__(self, **kwargs):
        """
        Initialize a Floor tile.

        Args:
            **kwargs: Passed to base Entity constructor.
        """
        super().__init__(**kwargs)