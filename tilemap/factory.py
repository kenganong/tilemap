def create_line_map(length):
  return LineMap(length)
def create_rectangle_map(width, height):
  return RectRectMap(width, height)

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

class RectRectMap:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.cols = []
    for _ in range(width):
      self.cols.append([None for _ in range(height)])
  def exists(self, coor):
    x, y = coor
    return x > -1 and x < self.width and y > -1 and y < self.height
  def _require_coor(self, coor):
    if not self.exists(coor):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
  def _get(self, coor):
    # internal get assumes that coor is valid
    x, y = coor
    return self.cols[x][y]
  def get(self, coor):
    self._require_coor(coor)
    return self._get(coor)
  def set(self, coor, content):
    x, y = coor
    self._require_coor(coor)
    self.cols[x][y] = content
