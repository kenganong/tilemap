class GamePiece:
  def __init__(self, name, color):
    self.name = name
    self.color = color
  def __repr__(self):
    return '{} {}'.format(self.color, self.name)
  def __eq__(self, other):
    return (hasattr(other, 'name') and self.name == other.name
            and hasattr(other, 'color') and self.color == other.color)
  def __hash__(self):
    return hash((self.name, self.color))
