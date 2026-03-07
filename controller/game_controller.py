from model import *
from model.entities.characters.player import Player
from view import *

class GameController:
    @staticmethod
    def create_game():
        pass

    @staticmethod
    def start_game():
        pass

    @staticmethod
    def end_game():
        pass

    @staticmethod
    def create_player(name:str):
        return Player(name)