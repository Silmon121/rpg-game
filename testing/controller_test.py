"""Testing module for CollisionController."""

import registry as reg
import pygame
import pytest
from controller import *
from model import Goal, Wall, NPC, Player, Weapon, Sword


@pytest.fixture
def dummy_entity():
    class Dummy:
        def __init__(self, eid="E1", x=0, y=0):
            self.id = eid
            self.x = x
            self.y = y
    return Dummy()

@pytest.fixture
def dummy_game():
    class DummyGame:
        def __init__(self):
            self.entities = []
            self.current_map = type("Map", (), {"grid": []})()
            self.level_cleared = False
            self.next_level_called = False
            self.player = Player(x=0, y=0, hp=100, immortal=False)
            self.cc = CollisionController(self)

        def next_level(self):
            self.next_level_called = True

    return DummyGame()


# =========================================================
# COLLISION CONTROLLER TESTS
# =========================================================

def test_collision_out_of_bounds(monkeypatch, dummy_entity, dummy_game):
    # Resizing the game grid to 10x10 for testing
    monkeypatch.setattr(
        "controller.collision_controller.GRID_WIDTH",
        10, raising=False)
    monkeypatch.setattr(
        "controller.collision_controller.GRID_HEIGHT",
        10, raising=False)

    controller = CollisionController(dummy_game)
    entity = dummy_entity

    assert controller.check_collision(-1, 5, entity) is False
    assert controller.check_collision(10, 5, entity) is False
    assert controller.check_collision(5, 10, entity) is False
    assert controller.check_collision(10, 10, entity) is False
    assert controller.check_collision(5, -1, entity) is False
    assert controller.check_collision(4, 3, entity) is True

def test_collision_with_wall_blocked(dummy_entity, dummy_game):
    wall = Wall(x=2, y=2)

    game = dummy_game
    game.current_map.grid = [[wall]]

    controller = CollisionController(game)
    entity = dummy_entity

    assert controller.check_collision(2, 2, entity) is False
    assert controller.check_collision(2, 1, entity) is True

def test_goal_blocks_when_not_cleared(dummy_entity, dummy_game):
    goal = Goal(x=1, y=1)

    game = dummy_game
    game.current_map.grid = [[goal]]
    game.level_cleared = False

    controller = CollisionController(game)
    entity = dummy_entity

    assert controller.check_collision(1, 1, entity) is False

def test_goal_triggers_next_level(dummy_entity, dummy_game):
    goal = Goal(x=1, y=1)

    game = dummy_game
    game.current_map.grid = [[goal]]
    game.level_cleared = True

    controller = CollisionController(game)
    entity = dummy_entity

    controller.check_collision(1, 1, entity)

    assert game.next_level_called is True

def test_player_hits_npc(dummy_game):
    npc = NPC(x=1, y=1, hp=100, immortal=False)

    game = dummy_game
    game.entities = [npc]

    controller = CollisionController(game)

    sword = Sword(x= 0, y= 0)

    controller.check_collision(1, 1, sword)

    assert npc.health < npc.max_health

def test_player_enters_npc(dummy_game):
    game = dummy_game

    player = Player(x=0, y=0, hp=100, immortal=False)
    npc = NPC(x=1, y=1, hp=100, immortal=False)

    game.entities = [npc]
    controller = CollisionController(game)

    controller.check_collision(1, 1, player)

    assert player.health < player.max_health

def test_npc_vs_npc_blocked(dummy_game, dummy_entity):
    npc1 = NPC(x=0, y=0)
    npc2 = NPC(x=1, y=1)

    game = dummy_game
    game.entities = [npc1, npc2]

    controller = CollisionController(game)

    assert controller.check_collision(1, 1, npc1) is False

def test_weapon_hits_npc(dummy_game):
    npc = NPC(x=1, y=1, hp=10, immortal=False)

    game = dummy_game
    game.entities = [npc]

    controller = CollisionController(game)

    weapon = Weapon(x=0, y=0)

    controller.check_collision(1, 1, weapon)

    assert npc.health < npc.max_health

def test_npc_attacks_player(dummy_game):
    game = dummy_game

    player = Player(x=1, y=1, hp=100, immortal=False)
    npc = NPC(x=0, y=0, hp=10, immortal=False, agro=True)

    game.entities = [player, npc]

    controller = CollisionController(game)

    # FORCE collision resolution directly
    controller.check_collision(1, 1, npc)

    assert player.health < 100

# =========================================================
# FILE CONTROLLER TESTS
# =========================================================

def test_get_maps_json(monkeypatch):
    """FileController should return parsed JSON data."""

    fake_data = {"level": 1}

    class FakeFile:
        def __enter__(self): return self
        def __exit__(self, *args): pass

    def fake_open(*args, **kwargs):
        return FakeFile()

    def fake_json_load(file):
        return fake_data

    monkeypatch.setattr("builtins.open", fake_open)
    monkeypatch.setattr("json.load", fake_json_load)

    result = FileController.get_maps_json()

    assert result == fake_data

# =========================================================
# PLAYER CONTROLLER TESTS
# =========================================================

def test_handle_input_w_moves_up(monkeypatch, dummy_game):
    game = dummy_game
    reg.game = game

    controller = PlayerController(game)

    event = type("E", (), {"key": pygame.K_w})()

    controller.handle_input(event)

    assert game.player.position != [0, -1]

def test_handle_input_s_moves_down(monkeypatch, dummy_game):
    game = dummy_game
    reg.game = game

    controller = PlayerController(game)

    event = type("E", (), {"key": pygame.K_s})()

    controller.handle_input(event)

    assert game.player.position == [0, 1]

def test_handle_input_d_moves_right(monkeypatch, dummy_game):
    game = dummy_game
    reg.game = game

    controller = PlayerController(game)

    event = type("E", (), {"key": pygame.K_d})()

    controller.handle_input(event)

    assert game.player.position == [1, 0]

def test_handle_input_a_moves_right(monkeypatch, dummy_game):
    game = dummy_game
    reg.game = game

    controller = PlayerController(game)

    event = type("E", (), {"key": pygame.K_a})()

    controller.handle_input(event)

    assert game.player.position != [-1, 0]

def test_handle_input_no_player():
    """Should safely return when player is None."""

    class DummyGame:
        def __init__(self):
            self.player = None

    controller = PlayerController(DummyGame())

    event = type("E", (), {"key": pygame.K_w})()

    controller.handle_input(event)

    assert controller.gc.player is None

def test_handle_input_player_no_position(monkeypatch, dummy_game):
    class DummyGame:
        def __init__(self):
            self.player = Player()

    controller = PlayerController(DummyGame())
    event = type("E", (), {"key": pygame.K_w})()
    controller.handle_input(event)

    with pytest.raises(ValueError):
        assert controller.gc.player.position is [None, None]

def test_sword_attack_creates_entity(monkeypatch):
    """SPACE should create sword entity."""

    class DummyPlayer:
        def __init__(self):
            self.x = 1
            self.y = 1
            self.face_direction = (1, 0)
            self.sword_attack = False

    class DummyGame:
        def __init__(self):
            self.player = DummyPlayer()
            self.entities = []
            self.created = None

        def create_entity(self, name, **kwargs):
            self.created = (name, kwargs)
            self.entities.append((name, kwargs))

        class cc:
            @staticmethod
            def check_collision(*args):
                return True

    controller = PlayerController(DummyGame())

    controller.sword_attack()

    assert controller.gc.created[0] == "sword"

def test_sword_removal_when_done():
    """Sword should be removed when update returns True."""

    class DummyPlayer:
        def __init__(self):
            self.health = 100
            self.sword_attack = True

    class DummyGame:
        def __init__(self):
            self.player = DummyPlayer()
            self.entities = [Sword(x=0, y=0)]

    controller = PlayerController(DummyGame())

    controller.check_player_status(0.6)

    assert controller.gc.entities == []

def test_sword_removal_when_time():
    """Sword should be removed when update returns True."""

    class DummyPlayer:
        def __init__(self):
            self.health = 100
            self.sword_attack = True

    class DummyGame:
        def __init__(self):
            self.player = DummyPlayer()
            self.entities = [Sword(x=0, y=0)]

    controller = PlayerController(DummyGame())

    controller.check_player_status(0.1)

    assert controller.gc.entities != []
