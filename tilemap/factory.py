def create_line_map(length):
  return LineMap(length)

class LineMap:
  LEFT = -1
  RIGHT = 1
  DIRECTIONS = [LEFT, RIGHT]
  def __init__(self, size):
    self.tiles = [None for _ in range(size)]
  def exists(self, coor):
    return coor > -1 and coor < len(self.tiles)
  def _require_coor(self, coor):
    if not self.exists(coor):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
  def get(self, coor):
    self._require_coor(coor)
    return self.tiles[coor]
  def set(self, coor, content):
    self._require_coor(coor)
    self.tiles[coor] = content
  def adjacent(self, coor):
    self._require_coor(coor)
    for direction in self.DIRECTIONS:
      new_coor = coor + direction
      if self.exists(new_coor):
        yield (new_coor, self.tiles[new_coor])
