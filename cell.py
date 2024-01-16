from graphics import Line, Point

class Cell:
    def __init__(self, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        self._draw_wall(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), self.has_left_wall)
        self._draw_wall(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), self.has_right_wall)
        self._draw_wall(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), self.has_top_wall)
        self._draw_wall(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), self.has_bottom_wall)

    def _draw_wall(self, line, has_wall):
        self._win.draw_line(line, 'white' if has_wall == True else 'black')

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        fill_color = "gray" if undo else "red"
        line = Line(Point(*self._center()), Point(*to_cell._center()))
        self._win.draw_line(line, fill_color)

    def _center(self):
        return (self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2