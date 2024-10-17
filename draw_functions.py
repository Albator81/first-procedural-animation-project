from kivy.graphics import Color, Line, Ellipse
from typing import Tuple


def draw_circle(center_x: float, center_y: float, radius: float, color: Tuple[float, float, float, float], fill: bool = True, width: float = 4.0, outline: bool = True) -> None:
    Color(*color)
    pos = (center_x - radius, center_y - radius)
    size = (radius * 2, radius * 2)

    if fill:
        Ellipse(pos=pos, size=size)

        if outline:
            Color(0, 0, 0, 0.9)
            Line(circle=(center_x, center_y, radius), width=width)

    else:
        Line(circle=(center_x, center_y, radius), width=width)


def draw_line(points, color: Tuple[float, float, float, float], width: float = 3.0) -> None:
    Color(*color)
    Line(points=points, width=width)
