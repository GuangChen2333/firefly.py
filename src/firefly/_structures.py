class Rect:
    def __init__(self, left: int, top: int, width: int, height: int):
        self._left = left
        self._top = top
        self._width = width
        self._height = height

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __repr__(self):
        return f"Rect(left={self.left}, top={self.top}, width={self.width}, height={self.height})"

    def to_region(self):
        return self.left, self.top, self.width, self.height

    def __iter__(self):
        return iter(self.to_region())

class Position:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    @property
    def left(self) -> int:
        return self._left

    @property
    def top(self) -> int:
        return self._top

    @property
    def right(self) -> int:
        return self._right

    @property
    def bottom(self) -> int:
        return self._bottom

    def __repr__(self):
        return f"Position(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"

    def __iter__(self):
        return iter((self.left, self.top, self.right, self.bottom))
