from .context import tilemap
from tilemap import factory
from .common import GamePiece
import pytest

@pytest.fixture
def empty_map():
  return factory.create_rectangle_map(3, 4)

@pytest.fixture
def simple_map(empty_map):
  empty_map.set((1, 1), GamePiece('pawn', 'black'))
  empty_map.set((2, 0), GamePiece('bishop', 'white'))
  empty_map.set((0, 3), GamePiece('queen', 'black'))
  return empty_map

def test_get(simple_map):
  assert None == simple_map.get((0, 0))
  assert 'queen' == simple_map.get((0, 3)).name
  assert None == simple_map.get((2, 2))
  assert 'bishop' == simple_map.get((2, 0)).name
  assert 'pawn' == simple_map.get((1, 1)).name

def test_get_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.get((3, 1))
  with pytest.raises(IndexError):
    empty_map.get((2, 4))
  with pytest.raises(IndexError):
    empty_map.get((-1, 0))
  with pytest.raises(IndexError):
    empty_map.get((1, -1))
  empty_map.get((0, 0))
  empty_map.get((2, 3))
  empty_map.get((2, 0))
  empty_map.get((0, 3))

def test_set(empty_map):
  empty_map.set((2, 0), GamePiece('meeple', 'blue'))
  assert None == empty_map.get((0, 0))
  assert None != empty_map.get((2, 0))
  assert 'meeple' == empty_map.get((2, 0)).name

def test_set_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.set((0, -1), GamePiece('meeple', 'yellow'))
  with pytest.raises(IndexError):
    empty_map.set((-1, 0), GamePiece('pawn', 'white'))
  with pytest.raises(IndexError):
    empty_map.set((3, 1), GamePiece('bishop', 'black'))
  with pytest.raises(IndexError):
    empty_map.set((2, 4), GamePiece('shoe', 'silver'))
  with pytest.raises(IndexError):
    empty_map.set((6, 7), GamePiece('worker', 'purple'))
  # No errors
  empty_map.set((0, 0), GamePiece('cube', 'brown'))
  empty_map.set((2, 3), GamePiece('road', 'blue'))
