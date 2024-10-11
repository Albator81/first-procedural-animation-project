from kivy.app import App
from kivy.graphics import Color, Point, Line, Ellipse, ClearColor, ClearBuffers
from kivy.uix.widget import Widget
from kivy.utils import boundary
from kivy.vector import Vector


class Joint:
    def __init__(self, x=100, y=100, radius=25, color=(1, 0, 0), angle=0):
        self.x = x                   # X position of the joint
        self.y = y                   # Y position of the joint
        self.radius = radius          # Distance to the next joint
        self.color = color            # Color for rendering
        self.angle = angle            # Angle for joint rotation (optional)
        self.connections = []         # List of connected joints

    def attach(self, joint):
        """Attach another joint to this joint."""
        self.connections.append(joint)

    def is_leaf(self):
        """Check if this joint is a leaf (no attached joint)."""
        return len(self.connections) == 0  # No joints attached to it, but it can be attached to a joint

    def propagate_update_position(self, new_x, new_y):
        """Update the joint's position and adjust all connected joints."""
        # Set the new position for this joint
        self.x, self.y = new_x, new_y

        # Update positions of connected joints, except the one that caused this update
        for joint in self.connections:
            # Calculate vector from this joint to the connected joint
            v = Vector(joint.x - self.x, joint.y - self.y)
            distance = v.length()

            # Restrict movement based on allowed stretch
            stretch_limit = 1.30
            if distance > self.radius * stretch_limit or distance < self.radius / stretch_limit:
                # Normalize the v vector and scale it to the joint's radius
                v = v.normalize() * boundary(distance, self.radius / stretch_limit, self.radius * stretch_limit)
                joint.x = self.x + v.x
                joint.y = self.y + v.y

                # Recursively update the connected joints
                joint.propagate_update_position(joint.x, joint.y)

    def propagate_draw(self, canvas):
        """Draw the joint and all its connections on a widget canvas."""
        with canvas:
            Color(*self.color)
            Line(circle=(self.x, self.y, self.radius), width=3)
            Ellipse(pos=(self.x-2, self.y-2), size=(4, 4))
            # Draw lines to connected joints
            Color(0.7, 0.7, 0.7)
            for joint in self.connections:
                Line(points=[self.x, self.y, joint.x, joint.y], width=2)
                joint.propagate_draw(canvas)



class UpdateDrawWidget(Widget):
    joint = Joint(100, 100, 30, (1, 0, 0))
    # testing
    j = joint
    for i in range(1, 6):
        if not j.is_leaf():
            j = j.connections[0]
        j.attach(Joint(radius=40, color=(1, 0.2*i, 0.2*i)))

    def on_touch_move(self, touch):
        self.joint.propagate_update_position(touch.x, touch.y)
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
