"""View testing module."""

from view.sprite_loader import SpriteLoader
import pygame
from view.menu_view import MenuView

# =========================================================
# MAIN MENU TESTS
# =========================================================


def test_draw_text_does_not_crash(monkeypatch):
    """Test text drawing."""
    class FakeFont:
        def render(self, text, aa, color):
            return "surface"

    class FakeScreen:
        def blit(self, surface, pos):
            self.last = (surface, pos)

    class FakeView:
        SCREEN = FakeScreen()

    menu = MenuView(FakeView())

    menu.draw_text("Hello", FakeFont(), (255, 0, 0), 10, 20)

    assert menu.screen.last == ("surface", (10, 20))


def test_draw_main_menu_runs(monkeypatch):
    """Test main menu drawing."""
    class FakeFont:
        def render(self, text, aa, color):
            return "surface"

    class FakeScreen:
        def fill(self, color):
            self.filled = True

        def blit(self, surface, pos):
            pass

    class FakeView:
        SCREEN = FakeScreen()

    monkeypatch.setattr(pygame.font, "SysFont", lambda name, size: FakeFont())

    menu = MenuView(FakeView())

    menu.draw_main_menu()

    assert menu.screen.filled


def test_draw_outro_runs(monkeypatch):
    """Test outro menu drawing."""
    class FakeFont:
        def render(self, text, aa, color):
            return "surface"

    class FakeScreen:
        def fill(self, color):
            self.filled = True

        def blit(self, surface, pos):
            pass

    class FakeView:
        SCREEN = FakeScreen()

    monkeypatch.setattr(pygame.font, "SysFont", lambda name, size: FakeFont())

    menu = MenuView(FakeView())

    menu.draw_outro()

    assert menu.screen.filled

# =========================================================
# SPRITE LOADER
# =========================================================


def test_sprite_loader_initial_state():
    """Test sprite loader initialization."""
    loader = SpriteLoader()

    assert loader.wall_sprite is None
    assert loader.floor_sprite is None
    assert loader.player_sprite is None
    assert loader.light_elf_sprite is None
    assert loader.goal_door_sprite is None
    assert loader.goal_door_locked_sprite is None
    assert loader.sword_sprite is None
    assert loader.human_sprite is None
    assert loader.orc_sprite is None


def test_sprite_loader_load_sets_all_sprites(monkeypatch):
    """Test sprite loader loading all sprites."""
    loader = SpriteLoader()

    class FakeSurface:
        def convert_alpha(self):
            return self

    def fake_load(path):
        return FakeSurface()

    monkeypatch.setattr(pygame.image, "load", fake_load)

    loader.load()

    assert loader.wall_sprite is not None
    assert loader.floor_sprite is not None
    assert loader.player_sprite is not None
    assert loader.light_elf_sprite is not None
    assert loader.goal_door_sprite is not None
    assert loader.goal_door_locked_sprite is not None
    assert loader.sword_sprite is not None
    assert loader.human_sprite is not None
    assert loader.orc_sprite is not None
