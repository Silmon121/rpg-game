"""
Map module.

This module provides a basic representation of a game map using
a grid-based structure.
"""


class Map:
    """
    Represent a game map composed of a grid structure.

    The map stores a 2D grid describing the layout of tiles or objects
    and a unique identifier for reference.
    """

    def __init__(self, id: int, grid: list):
        """
        Initialize Map instance.

        Parameters
        ----------
        id : int
            Unique identifier of the map.
        grid : list
            Two-dimensional list representing map tiles or layout.
        """
        self.id = id
        self.grid = grid
