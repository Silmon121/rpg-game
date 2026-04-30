"""View testing module"""

from view.sprite_loader import SpriteLoader
import pygame

# =========================================================
# GAME VIEW TESTS
# =========================================================




# =========================================================
# MAIN MENU TESTS
# =========================================================




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
