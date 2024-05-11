import sys

import numpy as np
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout

from logic import constants
from logic.constants import PAINT_AREA_OFFSET_X, PAINT_AREA_OFFSET_Y, CELL_SIZE, FPS, RANDOM_RATIO
from logic.grid import Grid
from logic.simulation import SimulationThread
from ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Conway's Game of Life")

        self.width = constants.INIT_DRAW_WIDTH
        self.height = constants.INIT_DRAW_HEIGHT
        self.last_width = self.width
        self.last_height = self.height
        self.cell_size = CELL_SIZE
        self.widget_paint_area = Grid(self.width, self.height, self.cell_size)

        self.horizontalLayout = QHBoxLayout()
        self.widget_draw_area.setLayout(self.horizontalLayout)

        self.horizontalLayout.addWidget(self.widget_paint_area)
        self.widget_control_panel.setFixedWidth(200)

        self.simulation = SimulationThread(show_gens_label=self.label_show_gens)
        self.simulation.sig[QLabel].connect(self.widget_paint_area.simulation)

        self.lineEdit_gens_per_sec.setText(f"{FPS}")
        self.lineEdit_cell_size.setText(f"{CELL_SIZE}")
        self.lineEdit_random_ratio.setText(f"{RANDOM_RATIO}")
        self.comboBox_board_pattern.addItem('bordered')
        self.comboBox_board_pattern.addItem('donut')
        self.comboBox_board_pattern.setCurrentIndex(0)
        self.lineEdit_surface_width.setText(f"{self.width}")
        self.lineEdit_surface_height.setText(f"{self.height}")

        self.label_current_status.setText("Ready")
        self.checkBox_show_grid.setChecked(False)

    def resizeEvent(self, event):
        pass

    def closeEvent(self, event):
        self.simulation.flag = False
        self.simulation.wait()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.widget_paint_area.running:
            return
        if event.buttons() & Qt.MouseButton.LeftButton:
            """
                NoButton                 : Qt.MouseButton = ... # 0x0
                LeftButton               : Qt.MouseButton = ... # 0x1
                RightButton              : Qt.MouseButton = ... # 0x2
            """
            pos = event.position()
            row = (int(pos.y()) - PAINT_AREA_OFFSET_Y - 1) // self.cell_size
            col = (int(pos.x()) - PAINT_AREA_OFFSET_X - 1) // self.cell_size
            new_row = row + self.widget_paint_area.locate_start_location_vector[0]
            new_col = col + self.widget_paint_area.locate_start_location_vector[1]
            if (new_row, new_col) != self.widget_paint_area.last_toggled_cell:
                self.widget_paint_area.toggle_cell(row, col)
                self.widget_paint_area.update()

            in_area = PAINT_AREA_OFFSET_X < pos.x() < self.widget_paint_area.width + PAINT_AREA_OFFSET_X and PAINT_AREA_OFFSET_Y < pos.y() < self.widget_paint_area.height + PAINT_AREA_OFFSET_Y

            if (self.widget_paint_area.gens == 0 or self.widget_paint_area.gens == 1) and in_area:
                self.label_show_gens.setText("1")
                self.widget_paint_area.gens = 1
            return

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.RightButton:
            pos = event.position()
            in_area = PAINT_AREA_OFFSET_X < pos.x() < self.widget_paint_area.width + PAINT_AREA_OFFSET_X and PAINT_AREA_OFFSET_Y < pos.y() < self.widget_paint_area.height + PAINT_AREA_OFFSET_Y
            if in_area:
                self.widget_paint_area.mouse_right_button_pressed_pos = pos
        if self.widget_paint_area.running:
            return
        if event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.position()
            row = (int(pos.y()) - PAINT_AREA_OFFSET_Y - 1) // self.cell_size
            col = (int(pos.x()) - PAINT_AREA_OFFSET_X - 1) // self.cell_size
            self.widget_paint_area.toggle_cell(row, col)
            self.widget_paint_area.update()

            in_area = PAINT_AREA_OFFSET_X < pos.x() < self.widget_paint_area.width + PAINT_AREA_OFFSET_X and PAINT_AREA_OFFSET_Y < pos.y() < self.widget_paint_area.height + PAINT_AREA_OFFSET_Y

            if (self.widget_paint_area.gens == 0 or self.widget_paint_area.gens == 1) and in_area:
                self.label_show_gens.setText("1")
                self.widget_paint_area.gens = 1
            return

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.position()
            in_area = PAINT_AREA_OFFSET_X < pos.x() < self.widget_paint_area.width + PAINT_AREA_OFFSET_X and PAINT_AREA_OFFSET_Y < pos.y() < self.widget_paint_area.height + PAINT_AREA_OFFSET_Y
            if in_area:
                self.widget_paint_area.mouse_right_button_released_pos = pos

                self.widget_paint_area.grid_move_vector = self.widget_paint_area.get_delta_row_col(self.widget_paint_area.mouse_right_button_released_pos, self.widget_paint_area.mouse_right_button_pressed_pos)

                (self.widget_paint_area.overlapped_start_row_idx, self.widget_paint_area.overlapped_start_col_idx), \
                    (self.widget_paint_area.overlapped_end_row_idx, self.widget_paint_area.overlapped_end_col_idx), \
                    self.widget_paint_area.grid_move_vector \
                    = self.widget_paint_area.move_grid(
                    self.widget_paint_area.grid_move_vector,
                    (0, 0),

                    (self.widget_paint_area.rows - 1, self.widget_paint_area.cols - 1),
                    (self.widget_paint_area.overlapped_start_row_idx, self.widget_paint_area.overlapped_start_col_idx),
                    (self.widget_paint_area.overlapped_end_row_idx, self.widget_paint_area.overlapped_end_col_idx)
                )
                self.widget_paint_area.locate_start_location_vector = self.widget_paint_area.get_locate_start_location_vector(self.widget_paint_area.grid_move_vector)
                self.widget_paint_area.update()

    @Slot()
    def on_comboBox_board_pattern_currentIndexChanged(self):
        if self.comboBox_board_pattern.currentText() == 'bordered':
            self.widget_paint_area.survival_world = constants.Flag.Grid.survival_world_border
        if self.comboBox_board_pattern.currentText() == 'donut':
            self.widget_paint_area.survival_world = constants.Flag.Grid.survival_world_donut

    @Slot()
    def on_pushButton_next_step_clicked(self):
        if self.widget_paint_area.gens == 0:
            return
        self.widget_paint_area.running = False
        self.simulation.flag = False
        self.widget_paint_area.running = True
        self.widget_paint_area.simulation(label_show_gens=self.label_show_gens)
        self.widget_paint_area.running = False

    @Slot()
    def on_lineEdit_cell_size_editingFinished(self):
        if self.lineEdit_cell_size.text().isdigit():
            if int(self.lineEdit_cell_size.text()) > 100:
                self.cell_size = 100
                self.lineEdit_cell_size.setText("100")

            if int(self.lineEdit_cell_size.text()) < 5:
                self.cell_size = 5
                self.lineEdit_cell_size.setText("5")
            if 5 <= int(self.lineEdit_cell_size.text()) <= 100:
                self.cell_size = int(self.lineEdit_cell_size.text())
        else:
            try:
                if 5 <= float(self.lineEdit_cell_size.text()) <= 100:
                    self.cell_size = round(float(self.lineEdit_cell_size.text()), 0)
                    self.lineEdit_cell_size.setText(str(round(float(self.lineEdit_cell_size.text()))))
                    return
                if float(self.lineEdit_cell_size.text()) > 100:
                    self.cell_size = 100
                    self.lineEdit_cell_size.setText("100")
                    return
                if float(self.lineEdit_cell_size.text()) < 5:
                    self.cell_size = 5
                    self.lineEdit_cell_size.setText("5")
                    return
            except ValueError:
                self.cell_size = 10
                self.lineEdit_cell_size.setText("10")

        self.widget_paint_area.cell_size = self.cell_size
        self.widget_paint_area.rows = self.height // self.cell_size
        self.widget_paint_area.cols = self.width // self.cell_size
        self.widget_paint_area.overlapped_start_col_idx = 0
        self.widget_paint_area.overlapped_end_col_idx = self.widget_paint_area.cols - 1
        self.widget_paint_area.overlapped_start_row_idx = 0
        self.widget_paint_area.overlapped_end_row_idx = self.widget_paint_area.rows - 1
        self.widget_paint_area.cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.widget_paint_area.decorate_cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.on_pushButton_stop_clicked()
        self.widget_paint_area.is_resized = True
        self.widget_paint_area.update()

    @Slot()
    def on_lineEdit_random_ratio_editingFinished(self):
        try:
            if float(self.lineEdit_random_ratio.text()) >= 0.99:
                self.widget_paint_area.random_radio = 0.99
                self.lineEdit_random_ratio.setText("0.99")
            if float(self.lineEdit_random_ratio.text()) <= 0.01:
                self.widget_paint_area.random_radio = 0.01
                self.lineEdit_random_ratio.setText("0.01")
            if 0 < float(self.lineEdit_random_ratio.text()) < 1:
                self.widget_paint_area.random_radio = float(self.lineEdit_random_ratio.text())
        except ValueError:
            self.widget_paint_area.random_radio = 0.25
            self.lineEdit_random_ratio.setText("0.25")

    @Slot()
    def on_pushButton_clean_surface_clicked(self):
        self.widget_paint_area.clear()
        self.widget_paint_area.update()
        self.widget_paint_area.running = False
        self.simulation.flag = False
        self.simulation.quit()
        self.label_current_status.setText("Cleared")
        self.widget_paint_area.gens = 0
        self.label_show_gens.setText("")

    @Slot()
    def on_pushButton_start_clicked(self):
        if self.widget_paint_area.gens == 0:
            return
        self.widget_paint_area.running = True
        self.simulation.start()
        self.label_current_status.setText("Running")

    @Slot()
    def on_pushButton_stop_clicked(self):
        self.widget_paint_area.running = False
        self.simulation.flag = False
        self.simulation.quit()
        self.label_current_status.setText("Stopped")

    @Slot()
    def on_pushButton_random_gen_clicked(self):
        self.widget_paint_area.fill_random()
        self.label_show_gens.setText("1")
        self.widget_paint_area.gens = 1
        self.widget_paint_area.update()

    @Slot()
    def on_pushButton_reset_surface_position_clicked(self):
        self.widget_paint_area.overlapped_start_row_idx = 0
        self.widget_paint_area.overlapped_end_row_idx = self.widget_paint_area.rows - 1
        self.widget_paint_area.overlapped_start_col_idx = 0
        self.widget_paint_area.overlapped_end_col_idx = self.widget_paint_area.cols - 1
        self.widget_paint_area.grid_move_vector = (0, 0)
        self.widget_paint_area.locate_start_location_vector = (0, 0)
        self.widget_paint_area.update()

    def surface_width_height(self, width_height: str, line_edit_obj):
        if line_edit_obj.text().isdigit():
            if int(line_edit_obj.text()) > 2000:
                setattr(self, width_height, 2000)
                line_edit_obj.setText("2000")
            if int(line_edit_obj.text()) < 100:
                setattr(self, width_height, 100)
                line_edit_obj.setText("100")
            if 100 <= int(line_edit_obj.text()) <= 2000:
                setattr(self, width_height, int(line_edit_obj.text()))
        else:
            try:
                if 100 <= float(line_edit_obj.text()) <= 2000:
                    setattr(self, width_height, int(round(float(line_edit_obj.text()), 0)))
                    line_edit_obj.setText(str(round(float(line_edit_obj.text())))
                                          )
                    return
                if float(line_edit_obj.text()) > 2000:
                    setattr(self, width_height, 2000)
                    line_edit_obj.setText("2000")
                    return
                if float(line_edit_obj.text()) < 100:
                    setattr(self, width_height, 100)
                    line_edit_obj.setText("100")
                    return
            except ValueError:
                setattr(self, width_height, 800)
                line_edit_obj.setText("800")

    @Slot()
    def on_lineEdit_surface_width_editingFinished(self):
        self.surface_width_height("width", self.lineEdit_surface_width)
        if self.last_width == self.width:
            return
        else:
            self.last_width = self.width
        self.pushButton_clean_surface.click()
        self.widget_paint_area.width = self.width
        self.widget_paint_area.cols = self.width // self.cell_size
        self.widget_paint_area.overlapped_start_col_idx = 0
        self.widget_paint_area.overlapped_end_col_idx = self.widget_paint_area.cols - 1
        self.widget_paint_area.cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.widget_paint_area.decorate_cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.widget_paint_area.grid_move_vector = (0, 0)
        self.widget_paint_area.locate_start_location_vector = (0, 0)
        self.widget_paint_area.update()

    @Slot()
    def on_lineEdit_surface_height_editingFinished(self):
        self.surface_width_height("height", self.lineEdit_surface_height)
        if self.last_height == self.height:
            return
        else:
            self.last_height = self.height
        self.pushButton_clean_surface.click()
        self.widget_paint_area.height = self.height
        self.widget_paint_area.rows = self.height // self.cell_size
        self.widget_paint_area.overlapped_start_row_idx = 0
        self.widget_paint_area.overlapped_end_row_idx = self.widget_paint_area.rows - 1
        self.widget_paint_area.cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.widget_paint_area.decorate_cells = np.zeros((self.widget_paint_area.rows, self.widget_paint_area.cols), dtype=int)
        self.widget_paint_area.grid_move_vector = (0, 0)
        self.widget_paint_area.locate_start_location_vector = (0, 0)
        self.widget_paint_area.update()

    @Slot()
    def on_lineEdit_gens_per_sec_editingFinished(self):
        if self.lineEdit_gens_per_sec.text().isdigit():
            if int(self.lineEdit_gens_per_sec.text()) > 60:
                self.simulation.fps = 60
                self.lineEdit_gens_per_sec.setText("60")

            if int(self.lineEdit_gens_per_sec.text()) < 1:
                self.simulation.fps = 1
                self.lineEdit_gens_per_sec.setText("1")
            if 1 <= int(self.lineEdit_gens_per_sec.text()) <= 60:
                self.simulation.fps = int(self.lineEdit_gens_per_sec.text())

        else:
            try:
                if 60 >= float(self.lineEdit_gens_per_sec.text()) >= 0.5:
                    self.simulation.fps = round(float(self.lineEdit_gens_per_sec.text()), 0)
                    self.lineEdit_gens_per_sec.setText(str(round(float(self.lineEdit_gens_per_sec.text()))))
                    return

                if float(self.lineEdit_gens_per_sec.text()) > 60:
                    self.simulation.fps = 60
                    self.lineEdit_gens_per_sec.setText("60")
                    return
                if float(self.lineEdit_gens_per_sec.text()) < 0.5:
                    self.simulation.fps = 1
                    self.lineEdit_gens_per_sec.setText("1")
                    return
            except ValueError:
                self.simulation.fps = 12
                self.lineEdit_gens_per_sec.setText("12")

    @Slot()
    def on_checkBox_show_tail_stateChanged(self):
        self.widget_paint_area.show_tail = self.checkBox_show_tail.isChecked()

    @Slot()
    def on_pushButton_clear_tail_clicked(self):
        self.widget_paint_area.decorate_cells &= ~constants.Flag.Grid.show_tail
        self.widget_paint_area.update()

    @Slot()
    def on_checkBox_trace_1_gen_stateChanged(self):
        self.widget_paint_area.show_traces_of_death = self.checkBox_trace_1_gen.isChecked()

    @Slot()
    def on_checkBox_show_grid_stateChanged(self):
        self.widget_paint_area.show_grid = self.checkBox_show_grid.isChecked()
        self.widget_paint_area.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
