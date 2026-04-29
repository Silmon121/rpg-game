"""
Module that handles rendering the main menu.

Part of the game_view system.
"""

import pygame
from config import Color, MAIN_MENU_TEXT_FONT


class MenuView:
    """Class that handles rendering menus."""

    def __init__(self, game_view):
        """Initialize the main menu view."""
        self.vc = game_view
        self.screen = self.vc.SCREEN

    def draw_main_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(Color.BLUE)
        self.draw_text("The Way of The Ninja",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           40
                       ),
                       Color.RED,
                       225, 220
                       )
        self.draw_text("Blocky Edition",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           30
                       ),
                       Color.YELLOW,
                       325, 270
                       )
        self.draw_text("Press Space to play ...",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           30
                       ),
                       Color.WHITE,
                       275, 350
                       )

    def draw_outro(self):
        self.screen.fill(Color.BLUE)
        """Draw the outro screen."""
        self.draw_text("You have won the game!",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           40
                       ),
                       Color.YELLOW,
                       210, 230
                       )

        self.draw_text("Thank you for playing!",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           30
                       ),
                       Color.RED,
                       275, 300
                       )

        self.draw_text("Game by: Silmon121",
                       pygame.font.SysFont(
                           MAIN_MENU_TEXT_FONT,
                           25
                       ),
                       Color.WHITE,
                       310, 360
                       )

    def draw_text(self, text, font, text_color, x, y):
        """Draw a text on a screen."""
        display_text = font.render(text, True, text_color)
        self.vc.SCREEN.blit(display_text, (x, y))
