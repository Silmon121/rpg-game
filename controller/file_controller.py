"""
File I/O controller module.

Responsible for loading game data from external files,
such as maps, configuration, and saved state.
"""

import json


class FileController:
    """
    Handles file-based operations for the game.

    Available supports:
        - Loading map data from JSON files
    """

    def __init__(self):
        """Initialize the file controller."""
        pass

    @staticmethod
    def get_maps_json():
        """
        Load map data from JSON file.

        Returns:
            dict | list:
                Parsed JSON data from data/maps.json
        """
        with open("data/maps.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return data
