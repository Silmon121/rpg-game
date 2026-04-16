"""
Main game controller module.

This is the central orchestrator of the game lifecycle.

Responsible for:
- Initializing pygame and game window
- Managing the main game loop
- Handling user input events
- Creating and storing entities
- Loading and transforming maps
- Coordinating rendering and game systems
"""

import pygame
import registry
from .collision_controller import CollisionController
from .player_controller import PlayerController
from .file_controller import FileController
from model import Player, NPC, Wall, Floor, Map
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from view import GameView


class GameController:
    """
    Core controller of the entire game.

    Acts as the central coordinator between:
        - Input system
        - Entity system
        - Map system
        - Rendering system

    Holds global game state and runs the main loop.
    """

    #: Mapping of entity type names to their classes (factory pattern).
    __AVAILABLE_ENTITIES = {
        "player": Player,
        "npc": NPC,
    }

    def __init__(self):
        """
        Initialize the game controller and all core systems.

        Sets up:
            - Global registry reference
            - Pygame window and clock
            - Controllers (input, collision, file IO, rendering)
            - Game state variables
        """
        registry.game = self

        self.__initialize_pygame()
        self.__initialize_controllers()

        self.maps = self.fc.get_maps_json()
        self.current_map = None
        self.entities = []
        self.level = 1
        self.player = None
        self.running = True

    # =========================================================
    # Initialization
    # =========================================================

    def __initialize_controllers(self):
        """
        Initialize all subsystem controllers.

        Includes:
            - FileController: map/data loading
            - PlayerController: input handling
            - CollisionController: movement validation
            - GameView: rendering system
        """
        self.fc = FileController()
        self.pc = PlayerController()
        self.cc = CollisionController()
        self.gv = GameView(self.SCREEN)

    def __initialize_pygame(self):
        """Initialize pygame and create the main game window."""
        pygame.init()
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_TITLE)

    # =========================================================
    # Main game loop
    # =========================================================

    def run(self):
        """
        Run the main game loop.

        Handles:
            - Frame timing
            - Input processing
            - Rendering
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # delta time (currently unused)

            self.__handle_events()

            self.gv.draw_player(player=self.player)
            self.gv.render(
                player=self.player,
                game_map=self.current_map,
                entities=self.entities
            )

        pygame.quit()

    # =========================================================
    # Entity system
    # =========================================================

    def create_entity(self, e_name: str, **kwargs):
        """
        Create new entities.

        Args:
            e_name (str): Type of entity to create (e.g. 'player', 'npc')
            **kwargs: Arguments passed to entity constructor

        Returns:
            Entity: Created entity instance

        Raises:
            ValueError: If entity type is unknown
        """
        if e_name not in self.__AVAILABLE_ENTITIES:
            raise ValueError(
                f"Unknown entity type: {e_name}. "
                f"Available: {list(self.__AVAILABLE_ENTITIES.keys())}"
            )

        entity_class = self.__AVAILABLE_ENTITIES[e_name]
        entity = entity_class(**kwargs)

        self.entities.append(entity)
        return entity

    # =========================================================
    # Event handling
    # =========================================================

    def __handle_events(self):
        """
        Process all pygame input events.

        Handles:
            - Quit event
            - Escape key exit
            - Player input delegation
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.player is not None:
                    self.pc.handle_input(event)

    # =========================================================
    # Map system
    # =========================================================

    def select_map(self):
        """
        Load and select the current level map.

        Converts JSON map data into Map object and transforms
        tile data into game entities (walls, floors, NPCs, player).
        """
        if self.level > 0:
            current_map_dict = self.maps[str(self.level)]
            game_map = Map(current_map_dict["id"], current_map_dict["grid"])
            self.current_map = self.__transform_map(game_map)

    def __transform_map(self, map):
        """
        Convert raw map grid into game objects.

        Replaces:
            '1' → Wall
            '0' → Floor
            '2' → Player spawn
            'LE' → NPC spawn

        Args:
            map (Map): Raw map object

        Returns:
            Map: Transformed map with entities placed
        """
        for i in range(len(map.grid)):
            for j in range(len(map.grid[0])):

                cell = map.grid[i][j]

                if cell == '1':
                    map.grid[i][j] = Wall(x=i, y=j)

                elif cell == '0':
                    map.grid[i][j] = Floor(x=i, y=j)

                elif cell == '2':
                    player = self.create_entity("player", name="Ninja")
                    self.player = player
                    player.x = i
                    player.y = j
                    map.grid[i][j] = Floor(x=i, y=j)

                elif cell == 'LE':
                    entity = self.create_entity("npc", name="Elf")
                    entity.x = i
                    entity.y = j
                    map.grid[i][j] = Floor(x=i, y=j)

        return map
