from kivy.config import Config

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '720')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    persepcitive_point_x = NumericProperty(0)
    persepcitive_point_y = NumericProperty(0)

    V_NB_LINES = 10
    V_LINES_SPACING = .25  # percentage of display width
    vertical_lines = []

    H_NB_LINES = 10
    H_LINES_SPACING = .15  # percentage of display height
    horizontal_lines = []

    SPEED_Y = 4
    current_offset_y = 0

    SPEED_X = 15
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def on_parent(self, widget, parent):
        # print("ON_PARENT W: " + str(self.width) + " H: " + str(self.height))
        pass

    def on_size(self, *args):
        # print("ON_SIZE W: " + str(self.width) + " H: " + str(self.height))
        # self.persepcitive_point_x = self.width / 2
        # self.persepcitive_point_y = self.height * 0.75
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
        pass


    def on_perspective_point_x(self, widget, value):
        # print("PX: " + str(value))
        pass

    def on_perspective_point_y(self, widget, value):
        # print("PY: " + str(value))
        pass

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5

        for i in range(0, self.V_NB_LINES):
            line_x = central_line_x + offset * spacing + self.current_offset_x

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        central_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5

        xmin = central_line_x + offset * spacing + self.current_offset_x
        xmax = central_line_x - offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES):
            line_y = i * spacing_y - self.current_offset_y

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return int(x), int (y)

    def transform_perspective(self, x, y):
        lin_y = y * self.persepcitive_point_y / self.height
        if lin_y > self.persepcitive_point_y:
            lin_y = self.persepcitive_point_y

        diff_x = x - self.persepcitive_point_x
        diff_y = self.persepcitive_point_y - lin_y
        factor_y = diff_y / self.persepcitive_point_y
        factor_y = factor_y * factor_y

        tr_x = self.persepcitive_point_x + diff_x * factor_y
        tr_y = self.persepcitive_point_y - factor_y * self.persepcitive_point_y

        return int(tr_x), int(tr_y)

    def on_touch_down(self, touch):
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X

    def on_touch_up(self, touch):
        self.current_speed_x = 0

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED_Y * time_factor
        self.current_offset_x += self.current_speed_x * time_factor

        spacing_x = self.V_LINES_SPACING * self.width
        spacing_y = self.H_LINES_SPACING * self.height

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y

        if self.current_offset_x >= spacing_x:
            self.current_offset_x -= spacing_x
        # elif self.current_offset_x <= spacing_x:
        #     self.current_offset_x += spacing_x




class GalaxyApp(App):
    pass


GalaxyApp().run()
