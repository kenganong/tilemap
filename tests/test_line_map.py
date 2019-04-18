from .context import tilemap
from tilemap import factory
from .common import GamePiece
import pytest

@pytest.fixture
def empty_map():
  return factory.create_line_map(8)

@pytest.fixture
def simple_map(empty_map):
  empty_map.set(2, GamePiece('pawn', 'black'))
  empty_map.set(5, GamePiece('bishop', 'white'))
  return empty_map

def test_get(simple_map):
  assert None == simple_map.get(0)
  assert 'pawn' == simple_map.get(2).name
  assert 'bishop' == simple_map.get(5).name
  assert None == simple_map.get(7)

def test_get_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.get(8)
  with pytest.raises(IndexError):
    empty_map.get(-1)
  empty_map.get(0)
  empty_map.get(7)

def test_set(empty_map):
  assert None == empty_map.set(1, GamePiece('meeple', 'blue'))
  assert None == empty_map.get(0)
  assert None != empty_map.get(1)
  assert 'meeple' == empty_map.get(1).name
  assert None == empty_map.set(3, GamePiece('road', 'black'))
  assert GamePiece('meeple', 'blue') == empty_map.set(1, GamePiece('pawn', 'white'))
  assert GamePiece('pawn', 'white') == empty_map.set(1, GamePiece('bishop', 'black'))

def test_set_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.set(8, GamePiece('meeple', 'yellow'))
  with pytest.raises(IndexError):
    empty_map.set(-1, GamePiece('pawn', 'black'))
  with pytest.raises(IndexError):
    empty_map.set(-3, GamePiece('bishop', 'white'))
  # No errors
  empty_map.set(0, GamePiece('cube', 'brown'))
  empty_map.set(7, GamePiece('road', 'blue'))

def test_exists(simple_map):
  assert simple_map.exists(2)
  assert simple_map.exists(5)
  assert simple_map.exists(0)
  assert simple_map.exists(7)
  assert not simple_map.exists(8)
  assert not simple_map.exists(-2)

def test_adjacent(simple_map):
  assert {(0, None), (2, GamePiece('pawn', 'black'))} == set(simple_map.adjacent(1))
  assert {(5, GamePiece('bishop', 'white')), (7, None)} == set(simple_map.adjacent(6))
  assert {(1, None), (3, None)} == set(simple_map.adjacent(2))
  assert {(1, None),} == set(simple_map.adjacent(0))
  assert {(6, None),} == set(simple_map.adjacent(7))
  with pytest.raises(IndexError):
    next(simple_map.adjacent(-1))
  with pytest.raises(IndexError):
    next(simple_map.adjacent(8))

def test_tiles(simple_map):
  actual = list(simple_map.tiles())
  assert 8 == len(actual)
  assert (0, None) in actual
  assert (2, GamePiece('pawn', 'black')) in actual
  assert (4, None) in actual
  assert (5, GamePiece('bishop', 'white')) in actual

def test_move(simple_map):
  # Move piece to empty
  assert None == simple_map.move(2, 4)
  assert None == simple_map.get(2)
  assert GamePiece('pawn', 'black') == simple_map.get(4)
  # Move empty to empty
  assert None == simple_map.move(3, 1)
  assert None == simple_map.get(1)
  assert None == simple_map.get(3)
  # Move piece to piece
  assert GamePiece('pawn', 'black') == simple_map.move(5, 4)
  assert None == simple_map.get(5)
  assert GamePiece('bishop', 'white') == simple_map.get(4)
  # Move empty to piece
  assert GamePiece('bishop', 'white') == simple_map.move(1, 4)
  assert None == simple_map.get(1)
  assert None == simple_map.get(4)
  # End out of bounds
  simple_map.set(3, GamePiece('meeple', 'blue'))
  with pytest.raises(IndexError):
    simple_map.move(3, 9)
  assert GamePiece('meeple', 'blue') == simple_map.get(3)
  # Start out of bounds
  with pytest.raises(IndexError):
    simple_map.move(-1, 3)
  assert GamePiece('meeple', 'blue') == simple_map.get(3)
