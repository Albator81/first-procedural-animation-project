from typing import Tuple, Sequence
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


class AttachedJoints:
    def __init__(self, *joints: 'Joint') -> None:
        self.joints = list(joints)

    def attach(self, *joints) -> None:
        if len(joints) == 1:
            self.joints.append(joints[0])
        else:
            self.joints.extend(joints)

    def update(self, anchor_joint: 'Joint') -> None:
        for joint in self.joints:
            projected_point = project(anchor_joint.anchor_point, anchor_joint.radius, joint.anchor_point, anchor_joint.stretch_limit, anchor_joint.retract_limit)
            joint.update(projected_point)

    def draw(self, canvas, anchor_joint) -> None:
        for joint in self.joints:
            with canvas:
                anchor_joint._draw_link(joint)
            joint.draw(canvas)


class Joint:
    def __init__(self, x: float = 100.0, y: float = 100.0, radius: float = 25.0, color: Tuple[float, float, float, float] = (1.0, 0.0, 0.0, 1.0), angle: float = 0.0, stretch_limit: float = 1.10, retract_limit: float = 0.90,):
        '''
        ``stretch_limit`` interval: [1;+inf[ 
        ``retract_limit`` interval: ]0;1]
        '''
        self.anchor_point = Point(x, y)
        self.radius = radius
        self.color = color
        self.angle = angle
        self.stretch_limit = stretch_limit
        self.retract_limit = retract_limit
        self.attached_joints = AttachedJoints()

    def attach(self, joint: 'Joint') -> None:
        if joint is self:
            raise RecursionError("you tried to attach a joint to itself")
        self.attached_joints.attach(joint)

    def has_attached_joints(self) -> bool:
        return len(self.attached_joints.joints) != 0

    def update(self, new_point: Point) -> None:
        if new_point != self.anchor_point:
            self.anchor_point = new_point
            self.attached_joints.update(self)

    def _draw_link(self, joint: 'Joint') -> None:
        draw_line(
            (self.anchor_point.x, self.anchor_point.y, joint.anchor_point.x, joint.anchor_point.y),
            (0.6, 0.52, 0.5, 0.4)
        )

    def _draw_distance_constraint(self, fill: bool = True, width: float = 8.0, outline: bool = True) -> None:
        draw_circle(
            self.anchor_point.x,
            self.anchor_point.y,
            self.radius,
            self.color,
            fill,
            width,
            outline
        )

    def _draw_anchor(self, radius: float = 8.0, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), width: float = 3.0, outline: bool = True) -> None:
        draw_circle(
            self.anchor_point.x,
            self.anchor_point.y,
            radius,
            color,
            True,
            width, 
            outline=outline
        )

    def draw(self, canvas) -> None:
        self.attached_joints.draw(canvas, self)
        with canvas:
            self._draw_distance_constraint(fill=False, width=self.radius / 11)
            self._draw_anchor(radius=self.radius / 4, width=self.radius / 11)
