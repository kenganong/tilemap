from .context import tilemap
from tilemap import factory
from .common import GamePiece
import pytest

@pytest.fixture
def zero_map():
  return factory.create_rectangle_hex_map(0, 0)

@pytest.fixture
def one_map():
  return factory.create_rectangle_hex_map(1, 1)

#     (0,0) (1,0) (2,0)
# (-1,1) (0,1) (1,1)
#    (-1,2) (0,2) (1,2)
# (-2,3) (-1,3) (0,3)

@pytest.fixture
def empty_map():
  return factory.create_rectangle_hex_map(3, 4)

@pytest.fixture
def simple_map(empty_map):
  empty_map.set((0, 1), GamePiece('pawn', 'black'))
  empty_map.set((-1, 2), GamePiece('bishop', 'white'))
  empty_map.set((0, 3), GamePiece('queen', 'black'))
  return empty_map

def test_get(simple_map):
  assert None == simple_map.get((0, 0))
  assert 'queen' == simple_map.get((0, 3)).name
  assert None == simple_map.get((1, 2))
  assert 'bishop' == simple_map.get((-1, 2)).name
  assert 'pawn' == simple_map.get((0, 1)).name

def test_get_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.get((2, 1))
  with pytest.raises(IndexError):
    empty_map.get((0, 4))
  with pytest.raises(IndexError):
    empty_map.get((-1, 0))
  with pytest.raises(IndexError):
    empty_map.get((-3, 3))
  empty_map.get((0, 0))
  empty_map.get((-2, 3))
  empty_map.get((2, 0))
  empty_map.get((0, 3))

def test_set(empty_map):
  empty_map.set((2, 0), GamePiece('meeple', 'blue'))
  assert None == empty_map.get((0, 0))
  assert None != empty_map.get((2, 0))
  assert 'meeple' == empty_map.get((2, 0)).name
  assert None == empty_map.set((1, 2), GamePiece('road', 'black'))
  assert GamePiece('meeple', 'blue') == empty_map.set((2, 0), GamePiece('pawn', 'white'))
  assert GamePiece('pawn', 'white') == empty_map.set((2, 0), GamePiece('bishop', 'black'))

def test_set_out_of_bounds(empty_map):
  with pytest.raises(IndexError):
    empty_map.set((0, -1), GamePiece('meeple', 'yellow'))
  with pytest.raises(IndexError):
    empty_map.set((-1, 0), GamePiece('pawn', 'white'))
  with pytest.raises(IndexError):
    empty_map.set((2, 1), GamePiece('bishop', 'black'))
  with pytest.raises(IndexError):
    empty_map.set((-2, 4), GamePiece('shoe', 'silver'))
  with pytest.raises(IndexError):
    empty_map.set((3, 1), GamePiece('worker', 'purple'))
  # No errors
  empty_map.set((0, 0), GamePiece('cube', 'brown'))
  empty_map.set((-1, 3), GamePiece('road', 'blue'))

def test_exists(simple_map):
  assert simple_map.exists((1, 1))
  assert simple_map.exists((2, 0))
  assert simple_map.exists((-1, 2))
  assert simple_map.exists((0, 0))
  assert not simple_map.exists((2, 2))
  assert not simple_map.exists((0, -1))

def test_adjacent(simple_map):
  # mids
  expected = {((0, 0), None), ((1, 0), None), ((-1, 1), None),
              ((1, 1), None), ((-1, 2), GamePiece('bishop', 'white')), ((0, 2), None)}
  assert expected == set(simple_map.adjacent((0, 1)))
  expected = {((0, 1), GamePiece('pawn', 'black')), ((1, 1), None), ((-1, 2), GamePiece('bishop', 'white')),
              ((1, 2), None), ((-1, 3), None), ((0, 3), GamePiece('queen', 'black'))}
  assert expected == set(simple_map.adjacent((0, 2)))
  # sides
  expected = {((-1, 2), GamePiece('bishop', 'white')), ((0, 2), None), ((-2, 3), None), ((0, 3), GamePiece('queen', 'black'))}
  assert expected == set(simple_map.adjacent((-1, 3)))
  expected = {((-1, 1), None), ((0, 1), GamePiece('pawn', 'black')), ((0, 2), None), ((-2, 3), None), ((-1, 3), None)}
  assert expected == set(simple_map.adjacent((-1, 2)))
  # corners
  expected = {((1, 1), None), ((0, 2), None), ((0, 3), GamePiece('queen', 'black'))}
  assert expected == set(simple_map.adjacent((1, 2)))
  expected = {((-1, 2), GamePiece('bishop', 'white')), ((-1, 3), None)}
  assert expected == set(simple_map.adjacent((-2, 3)))
  # out-of-bounds
  with pytest.raises(IndexError):
    next(simple_map.adjacent((-2, 2)))
  with pytest.raises(IndexError):
    next(simple_map.adjacent((1, 3)))

def test_tiles(simple_map):
  actual = list(simple_map.tiles())
  assert 12 == len(actual)
  assert ((0, 0), None) in actual
  assert ((0, 1), GamePiece('pawn', 'black')) in actual
  assert ((-1, 3), None) in actual
  assert ((1, 2), None) in actual
  assert ((0, 3), GamePiece('queen', 'black')) in actual

def test_sides(zero_map, one_map, simple_map):
  actual = list(simple_map.sides())
  assert len(actual) == 10
  assert ((0, 0), None) in actual
  assert ((-1, 2), GamePiece('bishop', 'white')) in actual
  assert ((1, 1), None) in actual
  actual = list(zero_map.sides())
  assert len(actual) == 0
  actual = list(one_map.sides())
  assert len(actual) == 1
  assert ((0, 0), None) in actual
  tiny_map = factory.create_rectangle_hex_map(2, 2)
  actual = list(tiny_map.sides())
  assert len(actual) == 4
  assert ((-1, 1), None) in actual
  long_map = factory.create_rectangle_hex_map(5, 1)
  actual = list(long_map.sides())
  assert len(actual) == 5

def test_move(simple_map):
  # Move piece to empty
  assert None == simple_map.move((0, 1), (1, 2))
  assert None == simple_map.get((0, 1))
  assert GamePiece('pawn', 'black') == simple_map.get((1, 2))
  # Move empty to empty
  assert None == simple_map.move((1, 1), (0, 0))
  assert None == simple_map.get((1, 1))
  assert None == simple_map.get((0, 0))
  # Move piece to piece
  assert GamePiece('pawn', 'black') == simple_map.move((-1, 2), (1, 2))
  assert None == simple_map.get((-1, 2))
  assert GamePiece('bishop', 'white') == simple_map.get((1, 2))
  # Move empty to piece
  assert GamePiece('queen', 'black') == simple_map.move((-1, 1), (0, 3))
  assert None == simple_map.get((-1, 1))
  assert None == simple_map.get((0, 3))
  # End out of bounds
  with pytest.raises(IndexError):
    simple_map.move((1, 2), (3, 2))
  assert GamePiece('bishop', 'white') == simple_map.get((1, 2))
  # Start out of bounds
  with pytest.raises(IndexError):
    simple_map.move((-1, 0), (1, 2))
  assert GamePiece('bishop', 'white') == simple_map.get((1, 2))
