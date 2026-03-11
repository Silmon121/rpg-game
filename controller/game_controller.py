import pygame
from pywin.scintilla.bindings import assign_command_id

from controller.player_controler import PlayerController
from model import *
from view import *
from config import *

class GameController:
    __AVAILABLE_ENTITIES = {
        "player": Player,
        "npc": NPC,

    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = []
        self.player = None
        self.running = True
        pygame.display.set_caption(GAME_TITLE)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False
                        break;
                if self.player is not None:
                    PlayerController.handle_input(event, player=self.player)


    def create_entity(self, e_name: str, **kwargs):
        if e_name not in self.__AVAILABLE_ENTITIES:
            raise ValueError(f"Unknown entity type: {e_name}.\nPossible types: {list(self.__AVAILABLE_ENTITIES.keys())}")
        entity_class = self.__AVAILABLE_ENTITIES[e_name]
        entity = entity_class(**kwargs)
        self.entities.append(entity)
        self.assign_player()


    def assign_player(self):
        for entity in self.entities:
            if isinstance(entity, Player):
                self.player = entity