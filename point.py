from kivy.vector import Vector
from typing import Sequence, Union


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y
        self._xy = [x, y]

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value
        self._xy[0] = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value
        self._xy[1] = value

    @property
    def xy(self) -> list:
        return [self._x, self._y]

    @xy.setter
    def xy(self, value: Sequence[float]) -> None:
        if len(value) != 2:
            raise ValueError
        self._xy = self._x, self._y = [value[0], value[1]]

    def __add__(self, other: Union['Point','Vector']) -> 'Point':
        return Point(self._x + other.x, self._y + other.y)

    def __sub__(self, other: Union['Point','Vector']) -> 'Point':
        return Point(self._x - other.x, self._y - other.y)

    def __mul__(self, scalar: float) -> 'Point':
        return Point(self._x * scalar, self._y * scalar)

    def __truediv__(self, scalar: float) -> 'Point':
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return Point(self._x / scalar, self._y / scalar)

    def __eq__(self, other: 'Point') -> bool:
        return self._x == other.x and self._y == other.y

    def __repr__(self) -> str:
        return f"Point(x={self._x}, y={self._y})"
