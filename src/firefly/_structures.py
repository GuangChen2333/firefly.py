from typing import Tuple


class Rect:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rect(left={self.left}, top={self.top}, width={self.width}, height={self.height})"

    def to_region(self):
        return self.left, self.top, self.width, self.height

    def __iter__(self):
        return iter(self.to_region())

    def center(self):
        return Position.from_xy(
            self.left + int(self.width / 2),
            self.top + int(self.height / 2),
            self
        )


class Position:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @classmethod
    def from_xy(cls, x: int, y: int, rect: Rect):
        return cls(x, y, (rect.width - x), (rect.height - y))

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
    def __init__(self, rect: Rect, confidence: float):
        self._rect = rect
        self._confidence = confidence

    @property
    def rect(self):
        return self._rect

    @property
    def confidence(self):
        return self._confidence

    def __repr__(self):
        return f"MatchResult(rect={self.rect}, confidence={self.confidence})"
