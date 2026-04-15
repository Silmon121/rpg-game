import json

class FileController:
    def __init__(self):
        pass

    @staticmethod
    def get_maps_json():
        with open("data/maps.json", "r") as file:
            data = json.load(file)
        return data