from typing import Tuple


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

    @classmethod
    def from_xy(cls, x: int, y: int, rect: Rect):
        return cls(x, y, (rect.width - x), (rect.height - y))

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

    def to_xy(self) -> Tuple[int, int]:
        return self.left, self.top

    def to_abs_position(self, parent_rect: Rect):
        return Position.from_xy(
            self.left + parent_rect.left,
            self.top + parent_rect.top,
            parent_rect
        )


class MatchResult:
    def __init__(self, position: Position, confidence: float):
        self._position = position
        self._confidence = confidence

    @property
    def position(self):
        return self._position

    @property
    def confidence(self):
        return self._confidence

    def __repr__(self):
        return f"MatchResult(position={self.position}, confidence={self.confidence})"
