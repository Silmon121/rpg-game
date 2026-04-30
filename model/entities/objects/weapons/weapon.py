"""
Weapon entity module.

Provide a base class for weapon-type entities.
"""

from model.entities.entity import Entity


class Weapon(Entity):
    """
    Represent a generic weapon entity.

    Provide cooldown-based usage logic shared by all weapons.
    """

    #: Unique prefix for movable entities.
    __ID_PREFIX = "WPN"

    #: Expected constructor parameters.
    __EXPECTED_PARAMETERS: dict[str, type] = {}

    #: General max cooldown
    _max_cooldown = 0.5

    def __init__(self, **kwargs):
        """
        Initialize Weapon instance.

        Parameters
        ----------
        **kwargs
            Arguments passed to Entity constructor.
        """
        super().__init__(**kwargs)
        self._cooldown = self._max_cooldown
        self.ready = False

    def apply_cooldown(self, dt):
        """
        Update weapon cooldown.

        Decrease cooldown by the given delta time and update
        readiness state when cooldown reaches zero.

        Parameters
        ----------
        dt : float
            Time delta to subtract from cooldown.
        """
        self._cooldown -= dt
        self.ready = False

        if self._cooldown <= 0:
            self.ready = True

    def update(self, dt):
        """
        Update weapon state.

        Apply cooldown logic and return whether the weapon
        is ready for use.

        Parameters
        ----------
        dt : float
            Time delta used for update step.

        Returns
        -------
        bool
            True if weapon is ready, False otherwise.
        """
        self.apply_cooldown(dt)
        return self.ready

    @property
    def cooldown(self):
        """
        Return current cooldown value.

        Returns
        -------
        float
            Remaining cooldown time.
        """
        return self._cooldown
