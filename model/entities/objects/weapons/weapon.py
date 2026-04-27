"""Sword class module."""
from model import Entity


class Weapon(Entity):
    """Sword class."""

    #: Unique prefix for movable entities.
    __ID_PREFIX = "WPN"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: General max cooldown
    _max_cooldown = 0.5

    def __init__(self, **kwargs):
        """Initialize the Sword class."""
        super().__init__(**kwargs)
        self._cooldown = self._max_cooldown
        self.ready = False

    def apply_cooldown(self, dt):
        self._cooldown -= dt
        self.ready = False
        if self._cooldown <= 0:
            self.ready = True

@property
def cooldown(self):
    return self._cooldown
