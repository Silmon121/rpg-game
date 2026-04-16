"""
Game rendering module.

Responsible for drawing the game world, including the map, player,
entities, and debug visuals onto the screen using pygame.
"""

import config
import pygame
from config import TILE_SIZE
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

    def __init__(self, screen):
        """Initialize the game view."""
        self.SCREEN = screen
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

    def render(self, entities: list, player: Player, game_map: Map):
        """
        Render a full frame of the game.

        This includes clearing the screen, drawing the debug grid,
        rendering the map, player, and entities, then updating the display.
        """
        self.SCREEN.fill((0, 0, 0))
        self.__draw_grid()
        self.draw_map(game_map)
        self.draw_player(player=player)
        self.draw_entities(entities)
        pygame.display.flip()

    def draw_player(self, player: Player):
        """Draw the player sprite."""
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

    def draw_entities(self, entities: list):
        """Render dynamic entities such as NPCs."""
        for entity in entities:
            if isinstance(entity, NPC):
                rect = pygame.Rect(
                    entity.x * config.TILE_SIZE,
                    entity.y * config.TILE_SIZE,
                    config.TILE_SIZE,
                    config.TILE_SIZE
                )
                pygame.draw.rect(self.SCREEN, (50, 50, 50), rect)
