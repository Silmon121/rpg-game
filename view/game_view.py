"""
Game rendering module.

Responsible for drawing the game world, including the map, player,
entities, and debug visuals onto the screen using pygame.
"""

import config
import pygame
from config import TILE_SIZE
from model.entities.characters.light_elf import LightElf
from model.entities.objects.goal import Goal
from model.entities.objects.weapons.sword import Sword
from .sprite_loader import SpriteLoader
from .main_menu_view import MainMenuView
from model import Player, Map, Wall, Floor, NPC


class GameView:
    """
    Handle rendering of the game world.

    The GameView is responsible for drawing all visual elements,
    including the tile map, player, NPCs, and debug grid.
    It does not contain game logic or state updates.
    """

    def __init__(self, game_controller):
        """Initialize the game view."""
        self.gc = game_controller
        self.SCREEN = self.gc.SCREEN
        self.sl = SpriteLoader()
        self.mmv = MainMenuView(self.SCREEN)
        self.__draw_grid()

    def __draw_grid(self):
        """Draw grid of tiles for debugging and testing."""
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                rect = pygame.Rect(
                    x * config.TILE_SIZE,
                    y * config.TILE_SIZE,
                    config.TILE_SIZE,
                    config.TILE_SIZE
                )
                pygame.draw.rect(self.SCREEN, (50, 50, 50), rect, 1)

    def render(self):
        """
        Render a full frame of the game.

        This includes clearing the screen, drawing the debug grid,
        rendering the map, player, and entities, then updating the display.
        """
        self.SCREEN.fill((0, 0, 0))
        self.__draw_grid()
        self.draw_map(self.gc.current_map)
        self.draw_player(player=self.gc.player)
        self.draw_ui()
        self.draw_entities(self.gc.entities)
        pygame.display.flip()

    def draw_player(self, player: Player):
        """Draw the player sprite."""
        if player is None:
            return
        self.SCREEN.blit(
            self.sl.player_sprite,
            (player.x * TILE_SIZE, player.y * TILE_SIZE)
        )

    def draw_map(self, game_map: Map):
        """Render the tile-based map."""
        for row in game_map.grid:
            for cell in row:
                if not isinstance(cell, str):
                    x = cell.x * config.TILE_SIZE
                    y = cell.y * config.TILE_SIZE

                    if isinstance(cell, Wall):
                        self.SCREEN.blit(self.sl.wall_sprite, (x, y))
                    elif isinstance(cell, Floor):
                        self.SCREEN.blit(self.sl.floor_sprite, (x, y))
                    elif isinstance(cell, Goal):
                        if self.gc.level_cleared:
                            self.SCREEN.blit(self.sl.goal_door_sprite, (x, y))
                        else:
                            self.SCREEN.blit(self.sl.goal_door_locked_sprite, (x, y))

    def draw_entities(self, entities: list):
        """Render dynamic entities such as NPCs."""
        for entity in entities:
            if isinstance(entity, LightElf):
                x = entity.x * config.TILE_SIZE
                y = entity.y * config.TILE_SIZE

                self.SCREEN.blit(self.sl.light_elf_sprite, (x, y))
            elif isinstance(entity, Sword):
                x = entity.x * config.TILE_SIZE
                y = entity.y * config.TILE_SIZE

                self.SCREEN.blit(self.sl.sword_sprite, (x, y))

    def draw_ui(self):
        """Draw the game UI."""
        self.draw_health_bar(self.SCREEN, 0, 0, 200, 20, self.gc.player.health, self.gc.player.max_health)

    @staticmethod
    def draw_health_bar(surface, x, y, width, height, current, maximum):
        # Ratio
        ratio = current / maximum

        # Background
        pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height))

        # Foreground
        pygame.draw.rect(surface, (255, 0, 0), (x, y, width * ratio, height))