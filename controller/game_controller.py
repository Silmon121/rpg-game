import pygame

import config
import registry
from .collision_controller import CollisionController
from .player_controller import PlayerController
from .file_controller import FileController
from model import *
from config import *
from view import GameView

class GameController:
    __AVAILABLE_ENTITIES = {
        "player": Player,
        "npc": NPC,
    }

    def __init__(self):
        registry.game = self

        self.__initialize_pygame()
        self.__initialize_controllers()

        self.maps = self.fc.get_maps_json()
        self.current_map = None
        self.entities = []
        self.level = 1
        self.player = None
        self.running = True


    def __initialize_controllers(self):
        self.fc = FileController()
        self.pc = PlayerController()
        self.cc = CollisionController()
        self.gv = GameView(self.SCREEN)


    def __initialize_pygame(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(GAME_TITLE)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.__handle_events()
            self.gv.draw_player(player=self.player)
            self.gv.render(player=self.player, game_map=self.current_map, entities=self.entities)
        pygame.quit()


    def create_entity(self, e_name: str, **kwargs):
        if e_name not in self.__AVAILABLE_ENTITIES:
            raise ValueError(f"Unknown entity type: {e_name}.\nPossible types: {list(self.__AVAILABLE_ENTITIES.keys())}")

        entity_class = self.__AVAILABLE_ENTITIES[e_name]
        entity = entity_class(**kwargs)
        self.entities.append(entity)

        return entity


    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False
                if self.player is not None:
                    self.pc.handle_input(event)


    def select_map(self):
        if self.level > 0:
            current_map_dict = self.maps[str(self.level)]
            game_map = Map(current_map_dict["id"], current_map_dict["grid"])
            self.current_map = self.__transform_map(game_map)


    def __transform_map(self, map):
        for i in range(len(map.grid)):
            for j in range(len(map.grid[0])):
                if map.grid[i][j] == '1':
                    map.grid[i][j] = Wall(x=i, y=j)
                elif map.grid[i][j] == '0':
                    map.grid[i][j] = Floor(x=i, y=j)
                elif map.grid[i][j] == '2':
                    player = self.create_entity("player", name="Ninja")
                    self.player = player
                    player.x = i
                    player.y = j
                    map.grid[i][j] = Floor(x=i, y=j)
                elif map.grid[i][j] == 'LE':
                    entity = self.create_entity("npc", name="Elf")
                    self.entities.append(entity)
                    entity.x = i
                    entity.y = j
                    map.grid[i][j] = Floor(x=i, y=j)
        return map