from kivy.app import App
from kivy.graphics import ClearColor, ClearBuffers
from kivy.uix.widget import Widget
from joint import Joint
from point import Point


class UpdateDrawWidget(Widget):
    joint = Joint(100, 100, 45, (0.2, 0, 0))
    # testing
    m = 20
    j = joint
    for i in range(1, m):
        if  len(j.attached) != 0:
            # j.attach(Joint(r=20, c=(0.2*i, 1, 0.2*i)))
            j = j.attached[0]
        j.attach(Joint(r=45-i, c=(1-0.5/m*i, 0.1/m*i, 1-0.6/m*i)))

    def on_touch_move(self, touch):
        self.joint.update(Point(touch.x, touch.y))
        self.canvas.clear()
        with self.canvas:
            ClearColor(0.4, 0.2, 0.8, 1)
            ClearBuffers()
        self.joint.draw(self.canvas)


class MyApp(App):

    def build(self):
        parent = Widget()
        parent.add_widget(UpdateDrawWidget())
        return parent


if __name__ == '__main__':
    MyApp().run()
