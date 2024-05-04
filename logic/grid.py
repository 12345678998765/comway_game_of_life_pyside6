from abc import ABC, abstractmethod

import numpy as np
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QLabel
from scipy.signal import convolve2d

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
        self.cells = np.zeros((self.rows, self.cols), dtype=int)
        self.convolved_result = np.zeros((self.rows, self.cols), dtype=int)
        self.cells_after_simulation = np.zeros((self.rows, self.cols), dtype=int)
        self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)
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
        self.kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])

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
        self.cells = np.random.rand(self.rows, self.cols) < self.random_radio
        self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)

    def clear(self):
        self.cells = np.zeros((self.rows, self.cols), dtype=int)
        self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)

    def simulation(self, label_show_gens: QLabel):
        if self.running:
            if self.convolved_result.shape[0] != self.rows or self.convolved_result.shape[1] != self.cols:
                self.convolved_result = np.zeros((self.rows, self.cols), dtype=int)
                self.cells_after_simulation = np.zeros((self.rows, self.cols), dtype=int)
            if self.survival_world & constants.Flag.Grid.survival_world_border:
                self.convolved_result = convolve2d(self.cells, self.kernel, mode='same', boundary='fill', fillvalue=0)
                self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result < 2) | (self.convolved_result > 3))] = 0
                self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result == 2) | (self.convolved_result == 3))] = 1
                self.cells_after_simulation[(self.cells == 0) & (self.convolved_result == 3)] = 1
                self.cells_after_simulation[(self.cells == 0) & (self.convolved_result != 3)] = 0
            elif self.survival_world & constants.Flag.Grid.survival_world_donut:
                self.convolved_result = convolve2d(self.cells, self.kernel, mode='same', boundary='wrap')
                self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result < 2) | (self.convolved_result > 3))] = 0
                self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result == 2) | (self.convolved_result == 3))] = 1
                self.cells_after_simulation[(self.cells == 0) & (self.convolved_result == 3)] = 1
                self.cells_after_simulation[(self.cells == 0) & (self.convolved_result != 3)] = 0

            if self.show_tail:
                self.decorate_cells[(self.cells == 1) & (self.cells_after_simulation == 0)] |= constants.Flag.Grid.show_tail
            if self.show_traces_of_death:
                self.decorate_cells[(self.cells == 1) & (self.cells_after_simulation == 0)] |= constants.Flag.Grid.show_traces_of_death
                self.decorate_cells[ \
                    (self.cells == 0) & \
                    (self.cells_after_simulation == 0) & \
                    (self.decorate_cells == constants.Flag.Grid.show_traces_of_death)] \
                    &= ~constants.Flag.Grid.show_traces_of_death
                self.decorate_cells[ \
                    (self.cells == 0) & \
                    (self.cells_after_simulation == 0) & \
                    (self.decorate_cells == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail))] \
                    &= ~constants.Flag.Grid.show_traces_of_death
            else:
                self.decorate_cells &= ~constants.Flag.Grid.show_traces_of_death

            self.cells = self.cells_after_simulation.copy()
            self.update()
            self.count_gens()
            label_show_gens.setText(str(self.gens))

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
