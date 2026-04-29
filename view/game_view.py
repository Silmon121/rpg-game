"""
Game rendering module.

Responsible for drawing the game world, including the map, player,
entities, and debug visuals onto the screen using pygame.
"""

import pygame
from config import TILE_SIZE, GRID_HEIGHT, GRID_WIDTH, Direction
from model import Wall, Floor, LightElf, Goal, Sword, Orc, Human
from .sprite_loader import SpriteLoader
from .menu_view import MenuView


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
        self.mv = MenuView(self)


    def render(self):
        """
        Render a full frame of the game.

        This includes clearing the screen, rendering the map,
        player, and entities, then updating the display.
        """
        if self.gc.level == -1:
            self.mv.draw_main_menu()
        elif self.gc.level == -2:
            self.mv.draw_outro()
        else:
            self._draw_level()

        # Update the window
        pygame.display.flip()

    def _draw_level(self):
        self.SCREEN.fill((0, 0, 0))
        self.__draw_map()
        self.__draw_player()
        self.__draw_hud()
        self.__draw_entities()

    def _draw_grid(self):
        """Draw grid of tiles for debugging and testing."""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(self.SCREEN,
                                 (50, 50, 50),
                                 rect, 1)

    def __draw_map(self):
        """Render the tile-based map."""
        game_map = self.gc.current_map

        if game_map is None:
            return
        for row in game_map.grid:
            for cell in row:
                if not isinstance(cell, str):
                    x = cell.x * TILE_SIZE
                    y = cell.y * TILE_SIZE

                    if isinstance(cell, Wall):
                        self.SCREEN.blit(self.sl.wall_sprite,
                                         (x, y))
                    elif isinstance(cell, Floor):
                        self.SCREEN.blit(self.sl.floor_sprite,
                                         (x, y))
                    elif isinstance(cell, Goal):
                        if self.gc.level_cleared:
                            self.SCREEN.blit(self.sl.goal_door_sprite,
                                             (x, y))
                        else:
                            self.SCREEN.blit(self.sl.goal_door_locked_sprite,
                                             (x, y))

    def __draw_entities(self):
        """Render dynamic entities such as NPCs ect."""
        entities = self.gc.entities

        for entity in entities:
            if isinstance(entity, LightElf):
                x = entity.x * TILE_SIZE
                y = entity.y * TILE_SIZE

                self.SCREEN.blit(self.sl.light_elf_sprite, (x, y))
            elif isinstance(entity, Orc):
                x = entity.x * TILE_SIZE
                y = entity.y * TILE_SIZE
                self.SCREEN.blit(self.sl.orc_sprite, (x, y))
            elif isinstance(entity, Human):
                x = entity.x * TILE_SIZE
                y = entity.y * TILE_SIZE

                self.SCREEN.blit(self.sl.human_sprite, (x, y))
            elif isinstance(entity, Sword):
                x = entity.x * TILE_SIZE
                y = entity.y * TILE_SIZE

                rotated_sword = self.sl.sword_sprite

                if self.gc.player.face_direction == Direction.LEFT:
                    rotated_sword = pygame.transform.rotate(rotated_sword,
                                                            Direction.LEFT_DEG)
                elif self.gc.player.face_direction == Direction.DOWN:
                    rotated_sword = pygame.transform.rotate(rotated_sword,
                                                            Direction.DOWN_DEG)
                elif self.gc.player.face_direction == Direction.UP:
                    rotated_sword = pygame.transform.rotate(rotated_sword,
                                                            Direction.UP_DEG)

                self.SCREEN.blit(rotated_sword, (x, y))

    def __draw_player(self):
        """Draw the player sprite."""
        player = self.gc.player

        if player is None:
            return
        self.SCREEN.blit(
            self.sl.player_sprite,
            (player.x * TILE_SIZE, player.y * TILE_SIZE)
        )

    def __draw_hud(self):
        """Draw the game HUD."""
        if self.gc.player is not None:
            self.__draw_health_bar(self.SCREEN,
                                   0, 0,
                                   200, 20,
                                   self.gc.player.health,
                                   self.gc.player.max_health)

    @staticmethod
    def __draw_health_bar(surface, x, y, width, height, current, maximum):
        """Draw the health bar."""
        # Ratio
        ratio = current / maximum

        # Background
        pygame.draw.rect(surface,
                         (0, 0, 0),
                         (x, y, width, height))

        # Foreground
        pygame.draw.rect(surface,
                         (255, 0, 0),
                         (x, y, width * ratio, height))
