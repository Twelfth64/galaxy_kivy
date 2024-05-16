from kivy.config import Config

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '720')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_down, on_keyboard_up, keyboard_closed, on_touch_down, on_touch_up
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
    current_y_loop = 0

    SPEED_X = 15
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 4
    tiles = []
    tiles_coordinates = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tile()
        self.generate_tiles_coordinates()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_tile(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def generate_tiles_coordinates(self):
        last_y = 0

        # clean the coordinates that are out of the screen
        # ti_y < self.current_y_loop

        for i in range(len(self.tiles_coordinates) -1, 0, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            self.tiles_coordinates.append((0, last_y))
            last_y += 1

    def get_line_x_from_index(self, index):
        central_line_x = self.persepcitive_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, xmax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = -int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(self.H_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES-1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.SPEED_Y * time_factor
        self.current_offset_x += self.current_speed_x * time_factor

        spacing_y = self.H_LINES_SPACING * self.height

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1
            self.generate_tiles_coordinates()





class GalaxyApp(App):
    pass


GalaxyApp().run()
