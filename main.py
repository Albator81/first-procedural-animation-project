from kivy.app import App
from kivy.graphics import ClearColor, ClearBuffers
from kivy.uix.widget import Widget
from joint import Joint
from point import Point
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config


Config.set('graphics', 'maxfps', '0')


class FPSLabel(Label):
    def __init__(self, **kwargs):
        super(FPSLabel, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60) # Update fps every second

    def update(self, dt):
        self.text = f"FPS: {Clock.get_rfps():.0f}"


class UpdateDrawWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.joint = Joint(100, 100, 45, (0.2, 0, 0))
        self.last_xy = (100, 100)
        ## testing
        m = 20
        j = self.joint
        for i in range(1, m):
            if  len(j.attached) != 0:
                # j.attach(Joint(r=20, c=(0.2*i, 1, 0.2*i)))
                j = j.attached[0]
            j.attach(Joint(r=45-i, c=(1-0.5/m*i, 0.1/m*i, 1-0.6/m*i)))
        ## end testing
        Clock.schedule_interval(self.update_draw, 1/20)

    def on_touch_down(self, touch):
        self.last_xy = touch.x, touch.y

    def on_touch_move(self, touch):
        self.last_xy = touch.x, touch.y

    def update_draw(self, dt):
        bf_p = self.joint.p.xy
        speed = 2*dt
        self.joint.update(Point(self.last_xy), speed, True)
        self.canvas.clear()
        if bf_p != self.joint.p.xy:
            with self.canvas:
                ClearColor(0.4, 0.2, 0.8, 1)
                ClearBuffers()
            self.joint.draw(self.canvas)


class MyApp(App):

    def build(self):
        parent = Widget()
        parent.add_widget(UpdateDrawWidget())
        parent.add_widget(FPSLabel())
        return parent


if __name__ == '__main__':
    MyApp().run()
