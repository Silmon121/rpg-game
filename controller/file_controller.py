"""
File I/O controller module.

Responsible for loading external game data,
such as maps, configuration files, and saved state.
"""

import json


class FileController:
    """
    Handle file-based operations for the game.

    This controller is responsible for loading and parsing
    external JSON data required by the game systems.
    """

    @staticmethod
    def get_maps_json():
        """
        Load map data from JSON file.

        The map file is read from:
            data/maps.json

        Returns
        -------
        dict | list
            Parsed JSON structure containing map data.
        """
        with open("data/maps.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return data
