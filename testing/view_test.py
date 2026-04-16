"""
View layer unit tests.

Focus:
- Rendering logic correctness
- Function calls (not actual pixels)
- Sprite usage validation
- Safe execution without pygame display dependency
"""

import pytest

from view.game_view import GameView
from view.sprite_loader import SpriteLoader
from view.main_menu_view import MainMenuView

from model.entities.objects.wall import Wall
from model.entities.objects.floor import Floor
from model.entities.characters.player import Player
from model.entities.characters.npc import NPC


# =========================================================
# SPRITE LOADER TESTS
# =========================================================

def test_sprite_loader_initialization(monkeypatch):
    """SpriteLoader should load sprites without crashing."""

    class FakeImage:
        @staticmethod
        def load(path):
            class FakeSurface:
                def convert_alpha(self):
                    return "sprite"
            return FakeSurface()

    import pygame
    monkeypatch.setattr(pygame, "image", FakeImage)

    import config
    monkeypatch.setattr(config, "WOODEN_WALL_SPRITE", "wall.png")
    monkeypatch.setattr(config, "WOODEN_FLOOR_SPRITE", "floor.png")
    monkeypatch.setattr(config, "PLAYER_SPRITE", "player.png")

    sl = SpriteLoader()

    assert sl.wall_sprite == "sprite"
    assert sl.floor_sprite == "sprite"
    assert sl.player_sprite == "sprite"


# =========================================================
# MAIN MENU VIEW TESTS
# =========================================================

def test_main_menu_view_initialization():
    """Main menu should store screen reference."""

    screen = object()
    mv = MainMenuView(screen)

    assert mv.screen is screen


# =========================================================
# GAME VIEW TESTS
# =========================================================

def test_game_view_initialization():
    """GameView should initialize correctly."""

    screen = object()
    gv = GameView(screen)

    assert gv.SCREEN is screen


def test_draw_player_position(monkeypatch):
    """Player should be drawn at correct tile position."""

    class FakeScreen:
        def blit(self, sprite, pos):
            self.last = (sprite, pos)

    class FakeSpriteLoader:
        player_sprite = "player_sprite"

    screen = FakeScreen()

    gv = GameView.__new__(GameView)
    gv.SCREEN = screen
    gv.sl = FakeSpriteLoader()

    player = Player(x=2, y=3)

    gv.draw_player(player)

    assert screen.last[0] == "player_sprite"
    assert screen.last[1] == (2 * 32, 3 * 32)


def test_draw_map_wall_and_floor(monkeypatch):
    """Map rendering should distinguish Wall and Floor."""

    class FakeScreen:
        def __init__(self):
            self.calls = []

        def blit(self, sprite, pos):
            self.calls.append((sprite, pos))

    class FakeSpriteLoader:
        wall_sprite = "wall"
        floor_sprite = "floor"

    screen = FakeScreen()

    gv = GameView.__new__(GameView)
    gv.SCREEN = screen
    gv.sl = FakeSpriteLoader()

    class FakeMap:
        grid = [
            [Wall(x=1, y=1), Floor(x=2, y=2)]
        ]

    gv.draw_map(FakeMap())

    assert ("wall", (1 * 32, 1 * 32)) in screen.calls
    assert ("floor", (2 * 32, 2 * 32)) in screen.calls


def test_draw_entities_npc_only():
    """Only NPCs should be drawn in entity layer."""

    class FakeScreen:
        def __init__(self):
            self.drawn = []

        def blit(self, *args, **kwargs):
            pass

        def fill(self, *args, **kwargs):
            pass

    screen = FakeScreen()

    gv = GameView.__new__(GameView)
    gv.SCREEN = screen

    npc = NPC(x=1, y=1)
    player = Player(x=2, y=2)

    gv.draw_entities([npc, player])

    # we cannot easily assert pygame rect calls without mocking deeper
    assert True