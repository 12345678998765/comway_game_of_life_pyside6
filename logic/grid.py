from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QWidget, QLabel
from scipy.signal import convolve2d

from logic import constants
from logic.constants import COLOR_ALIVE, COLOR_SURFACE, COLOR_TAIL, COLOR_DEAD


class Grid(QWidget):
    GridSE = tuple[tuple[int, int], tuple[int, int]]  # grid start-end points
    GridMoveVector = tuple[int, int]

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
        self.overlapped_start_row_idx = 0
        self.overlapped_end_row_idx = self.rows - 1
        self.overlapped_start_col_idx = 0
        self.overlapped_end_col_idx = self.cols - 1
        self.grid_move_vector = (0, 0)
        self.locate_start_location_vector = self.get_locate_start_location_vector(self.grid_move_vector)
        self.mouse_right_button_pressed_pos: Optional[QMouseEvent.position] = None
        self.mouse_right_button_released_pos: Optional[QMouseEvent.position] = None
        self.is_resized = False

    def resizeEvent(self, event):
        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size

    def get_state_painter_handler(self, adjusted_data_area_row_idx, adjusted_data_area_col_idx):
        if self.show_grid and self.cells[adjusted_data_area_row_idx][adjusted_data_area_col_idx]:
            state_painter_handler = self.state_painter["alive_with_grid"]
        elif self.show_grid and not self.cells[adjusted_data_area_row_idx][adjusted_data_area_col_idx]:
            state_painter_handler = self.state_painter["surface_with_grid"]
        elif not self.show_grid and self.cells[adjusted_data_area_row_idx][adjusted_data_area_col_idx]:
            state_painter_handler = self.state_painter["alive_no_grid"]
        elif not self.show_grid and not self.cells[adjusted_data_area_row_idx][adjusted_data_area_col_idx]:
            state_painter_handler = self.state_painter["surface_no_grid"]
        else:
            raise ValueError("Invalid state painter.")
        return state_painter_handler

    def paintEvent(self, event):
        painter = QPainter(self)
        point_to_start_location_vector_row_idx = self.locate_start_location_vector[0]
        point_to_start_location_vector_col_idx = self.locate_start_location_vector[1]
        for overlapped_area_row_idx in range(self.overlapped_start_row_idx, self.overlapped_end_row_idx + 1):
            for overlapped_area_col_idx in range(self.overlapped_start_col_idx, self.overlapped_end_col_idx + 1):
                if self.is_resized:
                    self.is_resized = False
                    self.cells = np.zeros((self.rows, self.cols), dtype=int)
                    self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)
                    self.update()
                    return
                else:
                    adjusted_data_area_row_idx = overlapped_area_row_idx + point_to_start_location_vector_row_idx
                    adjusted_data_area_col_idx = overlapped_area_col_idx + point_to_start_location_vector_col_idx
                    self.state_painter_handler = self.get_state_painter_handler(adjusted_data_area_row_idx, adjusted_data_area_col_idx)
                    self.state_painter_handler.paint(painter, self, overlapped_area_row_idx, overlapped_area_col_idx)

    def toggle_cell(self, row: int, col: int):
        new_row = row + self.locate_start_location_vector[0]
        new_col = col + self.locate_start_location_vector[1]
        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            self.cells[new_row][new_col] = not self.cells[new_row][new_col]
            self.last_toggled_cell = (new_row, new_col)

    def fill_random(self):
        self.cells = np.random.rand(self.rows, self.cols) < self.random_radio
        self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)

    def clear(self):
        self.cells = np.zeros((self.rows, self.cols), dtype=int)
        self.decorate_cells = np.zeros((self.rows, self.cols), dtype=int)

    def calc_convolve_result(self):
        if self.convolved_result.shape[0] != self.rows or self.convolved_result.shape[1] != self.cols:
            self.convolved_result = np.zeros((self.rows, self.cols), dtype=int)
            self.cells_after_simulation = np.zeros((self.rows, self.cols), dtype=int)
        if self.survival_world & constants.Flag.Grid.survival_world_border:
            self.convolved_result = convolve2d(self.cells, self.kernel, mode='same', boundary='fill', fillvalue=0)
        elif self.survival_world & constants.Flag.Grid.survival_world_donut:
            self.convolved_result = convolve2d(self.cells, self.kernel, mode='same', boundary='wrap')

    def calc_cells_after_simulation(self):
        self.calc_convolve_result()
        self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result < 2) | (self.convolved_result > 3))] = 0
        self.cells_after_simulation[(self.cells == 1) & ((self.convolved_result == 2) | (self.convolved_result == 3))] = 1
        self.cells_after_simulation[(self.cells == 0) & (self.convolved_result == 3)] = 1
        self.cells_after_simulation[(self.cells == 0) & (self.convolved_result != 3)] = 0

    def mark_tail(self):
        if self.show_tail:
            self.decorate_cells[(self.cells == 1) & (self.cells_after_simulation == 0)] |= constants.Flag.Grid.show_tail

    def mark_trace_of_death(self):
        if self.show_traces_of_death:
            self.decorate_cells[(self.cells == 1) & (self.cells_after_simulation == 0)] |= constants.Flag.Grid.show_traces_of_death
            self.decorate_cells[
                (self.cells == 0) &
                (self.cells_after_simulation == 0) &
                (self.decorate_cells == constants.Flag.Grid.show_traces_of_death)] \
                &= ~constants.Flag.Grid.show_traces_of_death
            self.decorate_cells[
                (self.cells == 0) &
                (self.cells_after_simulation == 0) &
                (self.decorate_cells == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail))] \
                &= ~constants.Flag.Grid.show_traces_of_death
        else:
            self.decorate_cells &= ~constants.Flag.Grid.show_traces_of_death

    def simulation(self, label_show_gens: QLabel):
        if self.running:
            self.calc_cells_after_simulation()
            self.mark_tail()
            self.mark_trace_of_death()
            self.cells = self.cells_after_simulation.copy()
            self.update()
            self.count_gens()
            label_show_gens.setText(str(self.gens))

    def count_gens(self):
        self.gens += 1
        return self.gens

    @staticmethod
    def get_locate_start_location_vector(grid_move_vector: GridMoveVector) -> GridMoveVector:
        return -grid_move_vector[0], -grid_move_vector[1]

    @staticmethod
    def get_last_synthesized_grid_move_vector(grid_1: GridSE, grid_2: GridSE) -> GridMoveVector:
        grid1_TopLeft, grid1_BottomRight = grid_1  # screen
        grid2_TopLeft, grid2_BottomRight = grid_2  # overlapped

        direction = [
            grid2_TopLeft[0] - grid1_TopLeft[0],
            grid2_TopLeft[1] - grid1_TopLeft[1],
            grid2_BottomRight[0] - grid1_BottomRight[0],
            grid2_BottomRight[1] - grid1_BottomRight[1],
        ]

        if direction[0] == 0 and direction[1] == 0 and direction[2] == 0 and direction[3] == 0:
            return 0, 0
        elif direction[0] == 0 and direction[1] == 0 and direction[2] == 0 and direction[3] != 0:
            # <--
            return 0, direction[3]
        elif direction[0] == 0 and direction[1] == 0 and direction[2] != 0 and direction[3] == 0:
            # ^
            # |
            return direction[2], 0
        elif direction[0] == 0 and direction[1] != 0 and direction[2] == 0 and direction[3] == 0:
            # -->
            return 0, direction[1]
        elif direction[0] != 0 and direction[1] == 0 and direction[2] == 0 and direction[3] == 0:
            # |
            # v
            return direction[0], 0
        elif direction[0] == 0 and direction[1] == 0 and direction[2] != 0 and direction[3] != 0:
            # ^
            # | <--
            return direction[2], direction[3]
        elif direction[0] != 0 and direction[1] != 0 and direction[2] == 0 and direction[3] == 0:
            # |
            # v -->
            return direction[0], direction[1]
        elif direction[0] != 0 and direction[1] == 0 and direction[2] == 0 and direction[3] != 0:
            # | <--
            # v
            return direction[0], direction[3]
        elif direction[0] == 0 and direction[1] != 0 and direction[2] != 0 and direction[3] == 0:
            # ^ -->
            # |
            return direction[2], direction[1]
        else:
            raise ValueError("Invalid direction.")

    def move_grid(self, grid_move_vector: GridMoveVector, origin_grid_TopLeft, origin_grid_BottomRight, overlapped_grid_TopLeft, overlapped_grid_BottomRight):
        last_synthesized_grid_move_vector = self.get_last_synthesized_grid_move_vector((origin_grid_TopLeft, origin_grid_BottomRight), (overlapped_grid_TopLeft, overlapped_grid_BottomRight))
        new_grid_move_vector = last_synthesized_grid_move_vector[0] + grid_move_vector[0], last_synthesized_grid_move_vector[1] + grid_move_vector[1]

        if new_grid_move_vector[0] < -(self.rows - 1):
            new_grid_move_vector = -(self.rows - 1), new_grid_move_vector[1]
        if new_grid_move_vector[0] > (self.rows - 1):
            new_grid_move_vector = self.rows - 1, new_grid_move_vector[1]
        if new_grid_move_vector[1] < -(self.cols - 1):
            new_grid_move_vector = new_grid_move_vector[0], -(self.cols - 1)
        if new_grid_move_vector[1] > (self.cols - 1):
            new_grid_move_vector = new_grid_move_vector[0], self.cols - 1

        self.grid_move_vector = new_grid_move_vector

        new_overlapped_grid_TopLeft = (
            min(max(0, origin_grid_TopLeft[0] + new_grid_move_vector[0]), self.rows - 1),
            min(max(0, origin_grid_TopLeft[1] + new_grid_move_vector[1]), self.cols - 1)
        )
        new_overlapped_grid_BottomRight = (
            max(min(self.rows - 1, origin_grid_BottomRight[0] + new_grid_move_vector[0]), 0),
            max(min(self.cols - 1, origin_grid_BottomRight[1] + new_grid_move_vector[1]), 0)
        )
        return new_overlapped_grid_TopLeft, new_overlapped_grid_BottomRight, new_grid_move_vector

    def get_delta_row_col(self, released_pos: QMouseEvent.position, pressed_pos: QMouseEvent.position):
        _delta_row = int(round(released_pos.y() - pressed_pos.y(), 0)) // self.cell_size
        _delta_col = int(round(released_pos.x() - pressed_pos.x(), 0)) // self.cell_size
        return _delta_row, _delta_col


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

    def paint(self, painter: QPainter, grid: Grid, paint_row, paint_col):
        data_row = paint_row + grid.locate_start_location_vector[0]
        data_col = paint_col + grid.locate_start_location_vector[1]
        if grid.decorate_cells[data_row][data_col] == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail):
            painter.fillRect(paint_col * grid.cell_size, paint_row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_DEAD)
        elif grid.decorate_cells[data_row][data_col] == constants.Flag.Grid.show_traces_of_death:
            painter.fillRect(paint_col * grid.cell_size, paint_row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_DEAD)
        elif grid.decorate_cells[data_row][data_col] == constants.Flag.Grid.show_tail:
            painter.fillRect(paint_col * grid.cell_size, paint_row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_TAIL)
        else:
            painter.fillRect(paint_col * grid.cell_size, paint_row * grid.cell_size, grid.cell_size, grid.cell_size, COLOR_SURFACE)


class PaintSurfaceWithGrid(IStatePainter):

    def paint(self, painter: QPainter, grid: Grid, paint_row, paint_col):
        data_row = paint_row + grid.locate_start_location_vector[0]
        data_col = paint_col + grid.locate_start_location_vector[1]
        if grid.decorate_cells[data_row][data_col] == (constants.Flag.Grid.show_traces_of_death | constants.Flag.Grid.show_tail):
            painter.fillRect(paint_col * grid.cell_size + 1, paint_row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_DEAD)
        elif grid.decorate_cells[data_row][data_col] == constants.Flag.Grid.show_traces_of_death:
            painter.fillRect(paint_col * grid.cell_size + 1, paint_row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_DEAD)
        elif grid.decorate_cells[data_row][data_col] == constants.Flag.Grid.show_tail:
            painter.fillRect(paint_col * grid.cell_size + 1, paint_row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_TAIL)
        else:
            painter.fillRect(paint_col * grid.cell_size + 1, paint_row * grid.cell_size + 1, grid.cell_size - 2, grid.cell_size - 2, COLOR_SURFACE)
