"""
Main game controller module.

This module acts as the central orchestrator of the game lifecycle.

It is responsible for:
- Initializing pygame and the game window
- Managing the main game loop
- Handling user input events
- Creating and managing entities
- Loading and transforming map data
- Coordinating rendering and subsystem controllers
"""

import pygame
import registry

from model import (
    Player, NPC, Wall, Floor, Map, Goal,
    LightElf, Weapon, Sword, Orc, Human
)

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from view import GameView
from .collision_controller import CollisionController
from .player_controller import PlayerController
from .file_controller import FileController


class GameController:
    """
    Core controller of the entire game.

    Acts as the central coordinator between:
        - Input system
        - Entity system
        - Map system
        - Rendering system

    Maintains global game state and executes the main game loop.
    """

    #: Mapping of entity type names to their corresponding classes.
    __AVAILABLE_ENTITIES = {
        "player": Player,
        "npc": NPC,
        "light_elf": LightElf,
        "orc": Orc,
        "human": Human,
        "sword": Sword
    }

    def __init__(self):
        """
        Initialize the game controller and all core systems.

        The following systems are initialized:
            - Pygame window and clock
            - File, input, collision, and rendering controllers
            - Global registry reference
            - Initial game state variables
        """
        #: Global registry reference for cross-module access.
        registry.game = self

        self.__initialize_pygame()
        self.__initialize_controllers()

        self.entities = []
        self.current_map = None
        self.player = None

        self.maps = self.fc.get_maps_json()

        self.level = -1  # -1 = main menu, -2 = outro
        self.level_cleared = False
        self.game_paused = True
        self.running = True

        self.select_map()

    # =========================================================
    # Initialization
    # =========================================================

    def __initialize_controllers(self):
        """
        Initialize subsystem controllers.

        The following controllers are created:
            - FileController (data loading)
            - PlayerController (player input handling)
            - CollisionController (movement validation)
            - GameView (rendering system)
        """
        self.fc = FileController()
        self.pc = PlayerController(self)
        self.cc = CollisionController(self)
        self.gv = GameView(self)

    def __initialize_pygame(self):
        """Initialize pygame and create the main game window."""
        pygame.init()
        self.SCREEN = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GAME_TITLE)

    # =========================================================
    # Main game loop
    # =========================================================

    def run(self):
        """
        Execute the main game loop.

        The loop handles:
            - Frame timing
            - Entity updates
            - Input processing
            - State evaluation
            - Rendering
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000

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
        Create and register a new entity.

        Parameters
        ----------
        e_name : str
            Type of entity to create (e.g. 'player', 'npc')
        **kwargs
            Arguments passed to the entity constructor.

        Returns
        -------
        Entity
            Created entity instance.

        Raises
        ------
        ValueError
            If the entity type is not registered.
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
        Process pygame input events.

        Handles:
            - Window close event
            - Escape key exit
            - Player input delegation
            - Main menu progression
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.level > 0 and self.player is not None:
                    self.pc.handle_input(event)

                elif self.level == -1 and event.key == pygame.K_SPACE:
                    self.level = 1
                    self.select_map()

    # =========================================================
    # Game State
    # =========================================================

    def __check_game_state(self):
        """Evaluate whether the current level is completed."""
        if any(isinstance(entity, NPC) for entity in self.entities):
            self.level_cleared = False
            return
        self.level_cleared = True

    def __update_entities(self, dt):
        """
        Update all active entities.

        Handles:
            - NPC movement updates
            - Weapon exclusion from generic update loop
            - Entity cleanup on death
        """
        for entity in self.entities[:]:
            if isinstance(entity, Weapon):
                continue

            if hasattr(entity, "health") and entity.health <= 0:
                self.entities.remove(entity)
                continue

            if isinstance(entity, NPC):
                entity.update_position(dt)

    # =========================================================
    # Map system
    # =========================================================

    def select_map(self):
        """
        Load and select the current level map.

        Converts JSON map data into a Map object and transforms
        grid cells into entities and terrain objects.
        """
        self.maps = self.fc.get_maps_json()

        current_map_dict = self.maps.get(str(self.level))

        if current_map_dict is None:
            if self.level != -1:
                self.level = -2
            return

        game_map = Map(current_map_dict["id"], current_map_dict["grid"])
        self.current_map = self._transform_map(game_map)

    def next_level(self):
        """Advance to the next level if the current one is cleared."""
        if self.level_cleared:
            self.level += 1
            self.restart_level()

    def restart_level(self):
        """Reset current level state and reload the map."""
        self.level_cleared = False

        self.entities.clear()
        self.player = None

        self.select_map()

    def _transform_map(self, game_map):
        """
        Convert raw map grid into game entities.

        Tile mapping:
            '1' → Wall
            '0' → Floor
            '2' → Player spawn
            'LE' → Light Elf
            'OR' → Orc
            'HU' → Human
            'G' → Goal

        Parameters
        ----------
        game_map : Map
            Raw map structure.

        Returns
        -------
        Map
            Transformed map with entities placed.
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

                elif cell == 'LE':
                    entity = self.create_entity("light_elf", name="Elf")
                    entity.x = i
                    entity.y = j
                    game_map.grid[i][j] = Floor(x=i, y=j)

                elif cell == 'OR':
                    entity = self.create_entity("orc", name="Orc")
                    entity.x = i
                    entity.y = j
                    game_map.grid[i][j] = Floor(x=i, y=j)

                elif cell == 'HU':
                    entity = self.create_entity("human", name="Human")
                    entity.x = i
                    entity.y = j
                    game_map.grid[i][j] = Floor(x=i, y=j)

                elif cell == 'G':
                    game_map.grid[i][j] = Goal(x=i, y=j)

        return game_map
