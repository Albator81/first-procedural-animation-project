from point import Point
from draw_functions import *
from kivy.utils import boundary
from kivy.vector import Vector


def project(circle_center: Point, radius: float, point: Point, stretch_limit: float, retract_limit: float) -> Point:
    projected_point = point * 1
    vector = Vector(point.x - circle_center.x, point.y - circle_center.y)
    distance = vector.length()

    if not distance == 0:
        min_distance = radius * retract_limit
        max_distance = radius * stretch_limit

        if distance > max_distance or distance < min_distance:
            adjusted_distance = boundary(distance, min_distance, max_distance)
            normalized_vector = vector.normalize() * adjusted_distance
            projected_point = circle_center + normalized_vector

    return projected_point


class Joint:
    def __init__(self, x=100.0, y=100.0, r=25.0, c=(1.0, 0.0, 0.0, 1.0), angle=0.0, s_lim=1.10, r_lim=0.90):
        self.p = Point(x, y)
        self.r = r
        self.c = c
        self.angle = angle
        self.s_lim = s_lim
        self.r_lim = r_lim
        self.attached = []

    def attach(self, joint):
        if joint is self:
            raise RecursionError("Can't attach a joint to itself")
        self.attached.append(joint)

    def update(self, new_p, speed: float = 1, progressive: bool = False):
        if progressive:
            new_p = self.p + (new_p - self.p) * speed
        queue = [(self, new_p)]
        while queue:
            joint, p = queue.pop(0)
            if p != joint.p:
                joint.p = p
            for j in joint.attached:
                proj_p = project(joint.p, joint.r, j.p, joint.s_lim, joint.r_lim)
                queue.append((j, proj_p))

    def draw(self, canvas):
        stack = [self]
        visited = set()
        while stack:
            joint = stack.pop()
            if joint in visited:
                continue
            visited.add(joint)
            for j in joint.attached:
                with canvas:
                    joint._draw_link(j)
                stack.append(j)
            with canvas:
                joint._draw_distance_constraint(fill=False, width=joint.r / 11)
                joint._draw_anchor(radius=joint.r / 4, width=joint.r / 11)

    def _draw_link(self, joint):
        draw_line((self.p.x, self.p.y, joint.p.x, joint.p.y), (0.6, 0.52, 0.5, 0.4))

    def _draw_distance_constraint(self, fill=True, width=8.0, outline=True):
        draw_circle(self.p.x, self.p.y, self.r, self.c, fill, width, outline)

    def _draw_anchor(self, radius=8.0, color=(1.0, 1.0, 1.0, 1.0), width=3.0, outline=True):
        draw_circle(self.p.x, self.p.y, radius, color, True, width, outline)
