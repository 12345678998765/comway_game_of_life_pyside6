from abc import ABC, abstractmethod
from random import random

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QLabel

from logic import constants
from logic.constants import COLOR_ALIVE, COLOR_SURFACE, COLOR_TAIL, COLOR_DEAD


class Grid(QWidget):
    def __init__(self, width, height, cell_size):
        super().__init__()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.cells = [[0 for _x in range(self.cols)] for _y in range(self.rows)]
        self.tmp_cells = [[0 for _x in range(self.cols)] for _y in range(self.rows)]
        self.decorate_cells = [[0 for _x in range(self.cols)] for _y in range(self.rows)]
        self.running = False
        self.last_toggled_cell = None
        self.random_radio = 0.25
        self.survival_world = constants.Flag.Grid.survival_world_border
        self.gens = 0
        self.show_grid = False
        self.state_painter = {
            "alive_no_grid": PaintAliveNoGrid(),
            "alive_with_grid": PaintAliveWithGrid(),
            "surface_no_grid": PaintSurfaceNoGrid(),
            "surface_with_grid": PaintSurfaceWithGrid(),
        }
        self.state_painter_handler = None
        self.show_tail = False
        self.show_traces_of_death = False

    def resizeEvent(self, event):
        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.show_grid and self.cells[row][col]:
                    self.state_painter_handler = self.state_painter["alive_with_grid"]
                elif self.show_grid and not self.cells[row][col]:
                    self.state_painter_handler = self.state_painter["surface_with_grid"]
                elif not self.show_grid and self.cells[row][col]:
                    self.state_painter_handler = self.state_painter["alive_no_grid"]
                elif not self.show_grid and not self.cells[row][col]:
                    self.state_painter_handler = self.state_painter["surface_no_grid"]
                else:
                    raise ValueError("Invalid state painter.")
                self.state_painter_handler.paint(painter, self, row, col)

    def toggle_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col] = not self.cells[row][col]
            self.last_toggled_cell = (row, col)

    def fill_random(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col] = random() < self.random_radio

    def clear(self):
        self.cells = [[0 for _x in range(self.width)] for _y in range(self.height)]
        self.decorate_cells = [[0 for _x in range(self.width)] for _y in range(self.height)]

    def simulation(self, label_show_gens: QLabel):
        if self.running:
            if len(self.tmp_cells) != self.rows or len(self.tmp_cells[0]) != self.cols:
                self.tmp_cells = [[0 for _x in range(self.cols)] for _y in range(self.rows)]
            for row in range(self.rows):
                for col in range(self.cols):
                    alive_neighbors = self.count_alive_neighbors(row, col)
                    if self.cells[row][col]:
                        # current cell is alive
                        if alive_neighbors < 2 or alive_neighbors > 3:
                            self.tmp_cells[row][col] = 0
                            if self.show_traces_of_death:
                                self.decorate_cells[row][col] |= constants.Flag.Grid.show_traces_of_death
                            else:
                                self.decorate_cells[row][col] &= ~constants.Flag.Grid.show_traces_of_death
                            if self.show_tail:
                                self.decorate_cells[row][col] |= constants.Flag.Grid.show_tail
                            # else:
                            #     self.decorate_cells[row][col] &= ~constants.Flag.Grid.show_tail
                        else:
                            self.tmp_cells[row][col] = 1
                    else:
                        # current cell is dead
                        if alive_neighbors == 3:
                            self.tmp_cells[row][col] = 1
                        else:
                            self.tmp_cells[row][col] = 0
                            if self.decorate_cells[row][col] & constants.Flag.Grid.show_traces_of_death:
                                self.decorate_cells[row][col] &= ~constants.Flag.Grid.show_traces_of_death

            self.cells = [[self.tmp_cells[y][x] for x in range(self.cols)] for y in range(self.rows)]
            self.update()
            self.count_gens()
            label_show_gens.setText(str(self.gens))

    def count_alive_neighbors(self, row, col):
        if self.survival_world & constants.Flag.Grid.survival_world_border:
            return self._count_alive_neighbors(row, col)
        elif self.survival_world & constants.Flag.Grid.survival_world_donut:
            return self._count_alive_neighbors_surround(row, col)
        else:
            raise ValueError("Invalid survival world.")

    def _count_alive_neighbors(self, row, col):
        alive_neighbors = 0
        for i in range(-1, 2):  # row offset of current cell
            for j in range(-1, 2):  # col offset of current cell
                if i == 0 and j == 0:
                    continue
                if 0 <= row + i < self.rows and 0 <= col + j < self.cols:  # check if the cell is out of bounds
                    alive_neighbors += self.cells[row + i][col + j]
        return alive_neighbors

    def _count_alive_neighbors_surround(self, row, col):
        alive_neighbors = 0
        for i in range(-1, 2):  # row offset of current cell
            for j in range(-1, 2):  # col offset of current cell
                if i == 0 and j == 0:
                    continue
                new_row = (row + i) % self.rows
                new_col = (col + j) % self.cols
                alive_neighbors += self.cells[new_row][new_col]
        return alive_neighbors

    def count_gens(self):
        self.gens += 1
        return self.gens


class IStatePainter(ABC):

    @abstractmethod
    def paint(self, painter: QPainter, grid: Grid, row: int, col: int):
        """Paint the grid with the given painter."""


class PaintAliveNoGrid(IStatePainter):

    def paint(self, painter: QPainter, grid: Grid, row, col):
        painter.fillRect(col * grid.cell_size, row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_ALIVE)


class PaintAliveWithGrid(IStatePainter):

    def paint(self, painter: QPainter, grid: Grid, row, col):
        painter.fillRect(col * grid.cell_size + 1, row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_ALIVE)


class PaintSurfaceNoGrid(IStatePainter):

    def paint(self, painter: QPainter, grid: Grid, row, col):
        if grid.decorate_cells[row][col] == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail):
            painter.fillRect(col * grid.cell_size, row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_DEAD)
        elif grid.decorate_cells[row][col] == constants.Flag.Grid.show_traces_of_death:
            painter.fillRect(col * grid.cell_size, row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_DEAD)
        elif grid.decorate_cells[row][col] == constants.Flag.Grid.show_tail:
            painter.fillRect(col * grid.cell_size, row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_TAIL)
        else:
            painter.fillRect(col * grid.cell_size, row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_SURFACE)


class PaintSurfaceWithGrid(IStatePainter):

    def paint(self, painter: QPainter, grid: Grid, row, col):
        if grid.decorate_cells[row][col] == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail):
            painter.fillRect(col * grid.cell_size + 1, row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_DEAD)
        elif grid.decorate_cells[row][col] == constants.Flag.Grid.show_traces_of_death:
            painter.fillRect(col * grid.cell_size + 1, row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_DEAD)
        elif grid.decorate_cells[row][col] == constants.Flag.Grid.show_tail:
            painter.fillRect(col * grid.cell_size + 1, row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_TAIL)
        else:
            painter.fillRect(col * grid.cell_size + 1, row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_SURFACE)
