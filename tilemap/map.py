class Map:
  def _require_coor(self, coor):
    if not self.exists(coor):
      raise IndexError('Coordinate {} outside tilemap bounds'.format(coor))
  def _shift_coor(self, coor, shift):
    return (coor[0] + shift[0], coor[1] + shift[1])
  def exists(self, coor):
    """Detects whether the given coordinate exists in the map

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      true or false, whether a tile with the given coordinate exists
    """
    raise NotImplementedError('Exists not yet implemented')
  def get(self, coor):
    """Gets the content of the tile at the given coordinate

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      tile contents

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    return self._get(coor)
  def set(self, coor, content):
    """Sets the content of the tile at the given coordinate

    Args:
      coor (tuple): the coordinate of the tile
      content: desired tile content

    Returns:
      prior tile contents

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    previous_content = self._get(coor)
    self._set(coor, content)
    return previous_content
  def tiles(self):
    """Traverses the map, getting all tiles within

    Returns:
      generator of (coor, content) tuples for all tiles
    """
    for coor in self.tile_coors():
      yield (coor, self._get(coor))
  def sides(self):
    """Gets the tiles on the edges of the map.
    A tile is on the side if at least one its borders is out-of-bounds.

    Returns:
      generator of (coor, content) tuples for all side tiles
    """
    for coor in self.side_coors():
      yield (coor, self._get(coor))
  def adjacent(self, coor):
    """Gets the tiles adjacent to the given coordinate

    Args:
      coor (tuple): the coordinate of the tile

    Returns:
      generator of (coor, content) tuples for all adjacent tiles

    Raises:
      IndexError when the given coordinate is outside the map
    """
    self._require_coor(coor)
    for _, direction in self.direction_map.items():
      new_coor = self._shift_coor(coor, direction)
      if self.exists(new_coor):
        yield (new_coor, self._get(new_coor))
  def move(self, start_coor, end_coor):
    """Moves the contents of the given start coordinate to the given end coordinate.
    Fills the start coordinate with empty and overwrites the contens of end coordinate.

    Args: 
      start_coor (tuple): the coordinate from which to move
      end_coor (tuple): the coordinate to which to move

    Returns:
      prior tile contents of end coordinate

    Raises:
      IndexError when either coordinate is outside the map
    """
    self._require_coor(end_coor) # check before we set start
    content = self.set(start_coor, None)
    return self.set(end_coor, content)
