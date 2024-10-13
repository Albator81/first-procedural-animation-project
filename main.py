from kivy.app import App
from kivy.graphics import Color, Point, Line, Ellipse, ClearColor, ClearBuffers
from kivy.uix.widget import Widget
from kivy.utils import boundary
from kivy.vector import Vector


def draw_circle(center_x, center_y, radius, color, fill=True, width=4, outline=True) -> None:
    Color(*color)
    if fill:
        Ellipse(pos=(center_x - radius, center_y - radius), size=(radius * 2, radius * 2))
        if outline:
            Color(0, 0, 0, 0.9)
            Line(circle=(center_x, center_y, radius), width=width)
    else:
        Line(circle=(center_x, center_y, radius), width=width)

def draw_line(start_x, start_y, end_x, end_y, color, width=3) -> None:
    Color(*color)
    Line(points=[start_x, start_y, end_x, end_y], width=width)

class Joint:
    def __init__(self, position_x=100, position_y=100, radius=25, color=(1, 0, 0), angle=0, stretch_limit=1.10, retract_limit=0.90):
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.angle = angle
        self.stretch_limit = stretch_limit   # interval: [1;+inf[
        self.retract_limit = retract_limit   # interval: ]0;1]
        self.color = color
        self.attached_joints = []

    def attach(self, joint):
        """Attach another joint to this joint."""
        self.attached_joints.append(joint)

    def is_leaf(self):
        """Check if this joint is a leaf (no attached joint)."""
        return len(self.attached_joints) == 0  # No joints attached to it, but it can be attached to a joint

    def stick(self, joint) -> bool:
        modified = False

        vector = Vector(joint.position_x - self.position_x, joint.position_y - self.position_y)
        distance = vector.length()

        if distance > self.radius * self.stretch_limit or distance < self.radius * self.retract_limit:
            vector = vector.normalize() * boundary(distance, self.radius * self.retract_limit, self.radius * self.stretch_limit)
            joint.position_x = self.position_x + vector.x
            joint.position_y = self.position_y + vector.y
            modified = True
        return modified

    def propagate_update_position(self, new_x, new_y):
        """Update the joint's position and adjust all connected joints."""
        self.position_x, self.position_y = new_x, new_y

        for joint in self.attached_joints:
            if self.stick(joint):
                joint.propagate_update_position(joint.position_x, joint.position_y)

    def _draw_link(self, joint):
        draw_line(self.position_x, self.position_y, joint.position_x, joint.position_y, (0.6, 0.52, 0.5, 0.4))

    def _draw_circle(self, fill=True, width=8, outline=True):
        draw_circle(self.position_x, self.position_y, self.radius, self.color, fill, width, outline)

    def _draw_point(self, radius=8, color=(1, 1, 1)):
        draw_circle(self.position_x, self.position_y, radius, color, outline=False)

    def propagate_draw(self, canvas):
        """Draw the joint and all its attached joints on a widget canvas."""
        with canvas:
            for joint in self.attached_joints:
                self._draw_link(joint)
                joint.propagate_draw(canvas)
            self._draw_circle(fill=False, width=self.radius // 7)
            self._draw_point(self.radius // 4)

class UpdateDrawWidget(Widget):
    joint = Joint(100, 100, 45, (0.2, 0, 0))
    # testing
    j = joint
    m = 20
    for i in range(1, m):
        if not j.is_leaf():
            # j.attach(Joint(radius=20, color=(0.2*i, 1, 0.2*i)))
            j = j.attached_joints[0]
        j.attach(Joint(radius=30, color=(1-0.5/m*i, 0.1/m*i, 1-0.6/m*i)))

    def on_touch_move(self, touch):
        self.joint.propagate_update_position(touch.x, touch.y)
        self.canvas.clear()
        with self.canvas:
            ClearColor(0.4, 0.2, 0.8, 1)
            ClearBuffers()
        self.joint.propagate_draw(self.canvas)


class MyApp(App):

    def build(self):
        parent = Widget()
        parent.add_widget(UpdateDrawWidget())
        return parent


if __name__ == '__main__':
    MyApp().run()
