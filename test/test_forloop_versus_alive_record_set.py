import functools
import time
from dataclasses import dataclass
import collections

import numpy as np


def timeit(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0
            for _ in range(times):
                start_time = time.time()
                ns = func(*args, **kwargs)
                total_time += time.time() - start_time
            print(f"Average time for {func.__name__}, size {args[0].shape[0]} x {args[0].shape[0]}: {total_time / times:.6f} s/step")
            return total_time / times

        return wrapper

    return decorator


@dataclass
class AliveRecord:
    name: str
    alive_cells: set[tuple[int, int]]


def get_pattern_from_ndarray(name: str, pattern: np.ndarray):
    alive_cells = set()
    for row in range(pattern.shape[0]):
        for col in range(pattern.shape[1]):
            if pattern[row][col]:
                alive_cells.add((row, col))
    return AliveRecord(name, alive_cells)


class LifeGrid:
    def __init__(self, pattern: AliveRecord):
        self.pattern = pattern

    @property
    def shape(self):
        return max(row for row, _ in self.pattern.alive_cells) + 1, max(col for _, col in self.pattern.alive_cells) + 1

    def evolve(self):
        neighbors = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        )

        alive_cells = collections.defaultdict(int)  # 0
        for row, col in self.pattern.alive_cells:
            for row_offset, col_offset in neighbors:
                alive_cells[(row + row_offset, col + col_offset)] += 1

        stay_alive = {cell for cell, count in alive_cells.items() if (count in {2, 3} and cell in self.pattern.alive_cells)}
        born = {cell for cell, count in alive_cells.items() if (count == 3 and cell not in self.pattern.alive_cells)}
        self.pattern.alive_cells = stay_alive | born
        return self.pattern.alive_cells

    def draw(self, start_row, start_col, end_row, end_col):
        display = [self.pattern.name.center(2 * (end_col - start_col))]
        for row in range(start_row, end_row + 1):
            display.append(
                "  ".join(
                    "X" if (row, col) in self.pattern.alive_cells else "."
                    for col in range(start_col, end_col)
                )
            )
        return "\n".join(display)

    def __str__(self):
        return (
            f"{self.pattern.name}\n"
            f"{sorted(self.pattern.alive_cells)}"
        )


@timeit(100)
def life_step_record_set(lg: LifeGrid):
    lg.evolve()


def count_alive_neighbors(row, col, rows, cols, cells):
    alive_neighbors = 0
    for i in range(-1, 2):  # row offset of current cell
        for j in range(-1, 2):  # col offset of current cell
            if i == 0 and j == 0:
                continue
            if 0 <= row + i < rows and 0 <= col + j < cols:  # check if the cell is out of bounds
                alive_neighbors += cells[row + i][col + j]
    return alive_neighbors


@timeit(100)
def life_step_for_loop(state):
    new_state = np.zeros_like(state)
    for row in range(state.shape[0]):
        for col in range(state.shape[1]):
            alive_neighbors = count_alive_neighbors(row, col, state.shape[0], state.shape[1], state)
            if state[row][col]:
                # current cell is alive
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_state[row][col] = 0
                else:
                    new_state[row][col] = 1
            else:
                # current cell is dead
                if alive_neighbors == 3:
                    new_state[row][col] = 1
                else:
                    new_state[row][col] = 0
    return new_state


if __name__ == "__main__":
    # glider = get_pattern_from_ndarray("Glider", np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]))
    # grid = LifeGrid(glider)
    # print(grid)
    # print(grid.draw(0, 0, 5, 5))
    # grid.evolve()
    # print(grid)
    # print(grid.draw(0, 0, 5, 5))

    grid_sizes = [10, 20, 50, 100, 200]

    np.random.seed(0)

    for grid_size in grid_sizes:
        state = np.zeros((grid_size, grid_size), dtype=int)

        for i in range(grid_size):
            for j in range(grid_size):
                state[i, j] = np.random.rand() < 0.25

        state_copy = state.copy()

        spend_time_forloop_avg = life_step_for_loop(state)

        state = state_copy.copy()

        spend_time_convolve_avg = life_step_record_set(LifeGrid(get_pattern_from_ndarray("Random", state)))
        print(f"About {spend_time_forloop_avg / spend_time_convolve_avg:.2f}x faster")
