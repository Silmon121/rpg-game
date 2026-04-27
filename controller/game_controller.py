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
from model.entities.characters.light_elf import LightElf
from model.entities.objects.goal import Goal
from model.entities.objects.weapons.sword import Sword
from model.entities.objects.weapons.weapon import Weapon
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
        "light_elf": LightElf,
        "sword": Sword
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

        #: Registry for remote access to the controller instance (e.g. for model)
        registry.game = self

        self.__initialize_pygame()
        self.__initialize_controllers()

        self.level_time = 0.0
        self.level_cleared = False

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
        self.pc = PlayerController(self)
        self.cc = CollisionController(self)
        self.gv = GameView(self)

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
            self.level_time += dt
            self.__update_entities(dt)
            self.__check_game_state()
            self.__handle_events()
            self.pc.check_player_status(dt)
            self.gv.render()

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

    def __update_entities(self, dt):
        for entity in self.entities:
            if not isinstance(entity, Weapon):
                if entity.health <= 0:
                    self.entities.remove(entity)
                    continue
                if isinstance(entity, NPC):
                    entity.update_position(dt)

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

    def __check_game_state(self):
        if NPC in self.entities:
            return
        self.level_cleared = True
    # =========================================================
    # Map system
    # =========================================================

    def select_map(self):
        """
        Load and select the current level map.

        Converts JSON map data into Map object and transforms
        tile data into game entities (walls, floors, NPCs, player).
        """
        self.maps = self.fc.get_maps_json()

        if self.level <= 0:
            return

        current_map_dict = self.maps.get(str(self.level))

        if current_map_dict is None:
            print(f"No map found for level {self.level}")
            return

        game_map = Map(current_map_dict["id"], current_map_dict["grid"])

        self.current_map = self.__transform_map(game_map)

    def next_level(self):
        if self.level_cleared:
            self.level += 1
            self.restart_level()

    def restart_level(self):
        self.level_cleared = False
        self.level_time = 0

        self.entities.clear()
        self.player = None

        self.select_map()

    def __transform_map(self, game_map):
        """
        Convert raw map grid into game objects.

        Replaces:
            '1' → Wall
            '0' → Floor
            '2' → Player spawn
            'LE' → Light elf spawn

        Args:
            game_map (Map): Raw map object

        Returns:
            Map: Transformed map with entities placed
        """

        for i in range(len(game_map.grid)):
            for j in range(len(game_map.grid[0])):

                cell = game_map.grid[i][j]

                if cell == '1':
                    game_map.grid[i][j] = Wall(x=i, y=j)

                elif cell == '0':
                    game_map.grid[i][j] = Floor(x=i, y=j)

                elif cell == '2':
                    player = self.create_entity("player", name="Ninja")
                    self.player = player
                    player.x = i
                    player.y = j
                    game_map.grid[i][j] = Floor(x=i, y=j)
                    if self.player is None:
                        raise Exception("Map has no player spawn ('2')")

                elif cell == 'LE':
                    entity = self.create_entity("light_elf", name="Elf")
                    entity.x = i
                    entity.y = j
                    game_map.grid[i][j] = Floor(x=i, y=j)

                elif cell == 'G':
                    game_map.grid[i][j] = Goal(x=i, y=j)

        return game_map
