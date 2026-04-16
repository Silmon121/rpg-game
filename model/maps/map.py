"""Module for map handling and representation."""


class Map:
    """
    Represents a game map composed of a grid structure.

    Attributes:
        id (int): Unique identifier for the map.
        grid (list): 2D structure representing the map layout.
    """

    def __init__(self, id: int, grid: list):
        """
        Initialize a Map instance.

        Args:
            id (int): Unique identifier for the map.
            grid (list): 2D list representing map tiles or layout.
        """
        self.id = id
        self.grid = grid
