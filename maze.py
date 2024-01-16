from cell import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            self._seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for j in range(self._num_rows)] for i in range(self._num_cols)]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        x1 = self._cell_size_x * i + self._x1
        y1 = self._cell_size_y * j + self._y1
        x2 = self._cell_size_x * (i + 1) + self._x1
        y2 = self._cell_size_y * (j + 1) + self._y1
        self._cells[i][j].draw(x1, y1, x2, y2)

        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.025)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[-1][-1]

        top_left_cell.has_top_wall = False
        self._draw_cell(0, 0)
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            choices = []
            if i > 0 and not self._cells[i - 1][j].visited:
                choices.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                choices.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                choices.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                choices.append((i, j + 1))
            
            if len(choices) == 0:
                self._draw_cell(i, j)
                return
            
            i2, j2 = random.choice(choices)
            if i2 > i:
                self._cells[i][j].has_right_wall = False
                self._cells[i2][j2].has_left_wall = False
            elif i2 < i:
                self._cells[i][j].has_left_wall = False
                self._cells[i2][j2].has_right_wall = False
            elif j2 > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i2][j2].has_top_wall = False
            elif j2 < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i2][j2].has_bottom_wall = False

            self._draw_cell(i, j)
            self._draw_cell(i2, j2)
            self._break_walls_r(i2, j2)
    
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        while True:
            choices = []
            if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
                choices.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
                choices.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_top_wall:
                choices.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_bottom_wall:
                choices.append((i, j + 1))
            
            if len(choices) == 0:
                return False
            
            i2, j2 = random.choice(choices)
            self._cells[i][j].draw_move(self._cells[i2][j2])
            if self._solve_r(i2, j2):
                return True
            self._cells[i][j].draw_move(self._cells[i2][j2], undo=True)