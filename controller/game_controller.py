import pygame
import registry
from .collision_controller import CollisionController
from .player_controler import PlayerController
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
        pygame.init()
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = []
        self.current_map = None
        self.level = 0
        self.player = None
        self.running = True
        self.pc = PlayerController()
        self.cc = CollisionController()
        self.gv = GameView(self.SCREEN)
        self.__load_maps()
        pygame.display.set_caption(GAME_TITLE)


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.__handle_events()

            self.gv.draw_player(player=self.player)
            self.gv.render(self.player, self.current_map)
        pygame.quit()

    def create_entity(self, e_name: str, **kwargs):
        if e_name not in self.__AVAILABLE_ENTITIES:
            raise ValueError(f"Unknown entity type: {e_name}.\nPossible types: {list(self.__AVAILABLE_ENTITIES.keys())}")

        entity_class = self.__AVAILABLE_ENTITIES[e_name]
        entity = entity_class(**kwargs)
        self.entities.append(entity)
        self.__assign_player()
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


    def __load_maps(self):
        self.create_entity(e_name="player", name="Hans", x=0, y=0)
        map = Map(id=1,
            grid=[
                 ['1','1','1','1','1','1','1','1','1','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','2','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','0','0','0','0','0','0','0','0','1'],
                 ['1','1','1','1','1','1','1','1','1','1']
                ]
        )
        for i in range(len(map.grid)):
            for j in range(len(map.grid[0])):
                if map.grid[i][j] == '1':
                    map.grid[i][j] = Wall(x=i, y=j)
                elif map.grid[i][j] == '0':
                    map.grid[i][j] = Floor(x=i, y=j)
                elif map.grid[i][j] == '2':
                    self.player.x = i
                    self.player.y = j
                    map.grid[i][j] = Floor(x=i, y=j)

        self.current_map = map


    def __assign_player(self):
        for entity in self.entities:
            if isinstance(entity, Player):
                self.player = entity