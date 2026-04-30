"""
Module that handles menu rendering.

Part of the game_view system.
"""

import pygame
from config import Color, MAIN_MENU_TEXT_FONT


class MenuView:
    """
    Menu rendering handler.

    This class is responsible for rendering menu-related screens,
    including the main menu and the outro screen displayed upon
    game completion.

    A reference to the GameView instance is stored to allow access
    to the main screen surface used for rendering.
    """

    def __init__(self, game_view):
        """
        Initialize MenuView instance.

        A reference to the provided GameView object is stored and
        the main screen surface is assigned for rendering operations.

        Parameters
        ----------
        game_view : GameView
            Game view instance providing access to the screen surface.
        """
        self.vc = game_view
        self.screen = self.vc.SCREEN

    def draw_main_menu(self):
        """
        Render main menu screen.

        The screen is filled with a background color and menu elements
        are drawn, including title text and start instructions.
        """
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
        """
        Render outro menu screen.

        The screen is filled with a background color and final game
        completion messages are displayed, including credits.
        """
        self.screen.fill(Color.BLUE)
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
        """
        Text is rendered onto the screen surface.

        The provided text is rendered using the given font and color,
        then displayed onto the screen at the specified coordinates.

        Parameters
        ----------
        text : str
            Text content to be rendered.
        font : pygame.font.SysFont
            Font object used for rendering.
        text_color : tuple or Color
            Color applied to the rendered text.
        x : int
            Horizontal position on the screen.
        y : int
            Vertical position on the screen.
        """
        display_text = font.render(text, True, text_color)
        self.vc.SCREEN.blit(display_text, (x, y))
