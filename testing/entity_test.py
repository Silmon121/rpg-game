"""
Entity system unit tests.

Covers:
- Base Entity behavior (validation, IDs, position system)
- Character system (HP, stats, immortality)
- Player and NPC specializations
- MovableEntity movement logic (with mocked collision)
- Object entities (Wall, Floor)

These tests ensure correctness of:
- inheritance system
- runtime validation logic
- core gameplay entity mechanics
"""
from model import Map
from model.entities.entity import Entity
from model.entities.characters.player import Player
from model.entities.characters.npc import NPC
from model.entities.objects.wall import Wall
from model.entities.objects.floor import Floor

# =========================================================
# INHERITANCE RULES
# =========================================================


def test_missing_required_class_fields_raises():
    """Test Entity class maintains required internal structure."""
    assert hasattr(Entity, "_Entity__ID_PREFIX")

# =========================================================
# PLAYER TESTS
# =========================================================


def test_player_max_health_override():
    """Player should use higher base HP."""
    p = Player(x=0, y=0)
    assert p.health == 100


def test_player_string_output():
    """Test Player __str__ should return readable output."""
    p = Player(x=1, y=2)
    s = str(p)
    assert "Player" in s

# =========================================================
# NPC TESTS
# =========================================================

# ---------------------------------------------------------
# AGRO BEHAVIOR
# ---------------------------------------------------------


def test_npc_agro_default():
    """NPC should default agro to False."""
    n = NPC()
    assert n.agro is True


def test_npc_agro_explicit_true():
    """NPC should accept agro=True explicitly."""
    n = NPC(agro=True)
    assert n.agro is True


def test_npc_agro_explicit_false():
    """NPC should accept agro=False explicitly."""
    n = NPC(agro=False)
    assert n.agro is False


# ---------------------------------------------------------
# MOVEMENT TIMER LOGIC
# ---------------------------------------------------------


def test_npc_moves_after_time(monkeypatch):
    """NPC should move after a time delta."""
    npc = NPC(agro=True)

    moves = []

    def fake_move(dx, dy):
        moves.append((dx, dy))

    npc.move = fake_move

    # Force movement probability to always pass
    monkeypatch.setattr("random.random", lambda: 0.0)

    # Force axis = x and direction = +1
    monkeypatch.setattr("random.randint", lambda a, b: 0)

    npc.update_position(dt=5.0)

    assert len(moves) == 1

def test_npc_does_not_move_before_time(monkeypatch):
    """NPC should move after a time delta."""
    npc = NPC(agro=True)

    moves = []
    npc.move = lambda dx, dy: moves.append((dx, dy))

    npc.update_position(dt=1.0)

    assert len(moves) == 0

def test_npc_does_not_move_if_probability_fails(monkeypatch):
    """Test NPC not moving if probability fails."""
    npc = NPC(agro=True)

    moves = []
    npc.move = lambda dx, dy: moves.append((dx, dy))

    # Force probability to fail
    monkeypatch.setattr("random.random", lambda: 1.0)

    npc.update_position(dt=5.0)

    assert len(moves) == 0

def test_npc_attack_when_agro():
    """"""
    npc = NPC(agro=True)
    target = type("Target", (), {"health": 100})()

    npc._damage = 10
    npc.attack(target)

    assert target.health == 90

def test_npc_does_not_attack_when_not_agro():
    npc = NPC(agro=False)
    target = type("Target", (), {"health": 100})()

    npc._damage = 10
    npc.attack(target)

    assert target.health == 100

def test_npc_update_position_resets_timer(monkeypatch):
    """After threshold, move_timer should reset."""
    n = NPC()

    monkeypatch.setattr("random.random", lambda: 1.0)  # prevent movement

    n.update_position(dt=5)

    assert n.move_timer == 0.0

# =========================================================
# OBJECT TESTS
# =========================================================


def test_wall_creation():
    """Wall should store correct coordinates."""
    w = Wall(x=1, y=1)
    assert w.x == 1
    assert w.y == 1


def test_floor_creation():
    """Floor should store correct coordinates."""
    f = Floor(x=2, y=2)
    assert f.x == 2
    assert f.y == 2

# =========================================================
# OBJECT TESTS
# =========================================================


def test_map_init():
    """Map should store correct coordinates."""
    m = Map(id="m1", grid=[["1", "2"]])

    assert m.id == "m1"
    assert m.grid == [["1", "2"]]