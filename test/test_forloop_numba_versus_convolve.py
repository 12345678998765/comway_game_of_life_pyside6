import functools
import time

import numpy as np
import scipy.signal as signal
from numba import jit


def timeit(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0
            for _ in range(times):
                start_time = time.time()
                ns = func(*args, **kwargs)
                total_time += time.time() - start_time
            print(f"Average time for {func.__name__}, size {args[0].shape[0]} x {args[0].shape[0]}: {total_time / times:.8f} s/step")
            return total_time / times

        return wrapper

    return decorator

@jit(nopython=True)
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
@jit(nopython=True)
def life_step_for_loop_numba(state):
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


@timeit(100)
def life_step_convolution(state):
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])

    convolution_state = signal.convolve2d(state, kernel, mode='same', boundary='fill', fillvalue=0)
    state[(state == 1) & ((convolution_state < 2) | (convolution_state > 3))] = 0
    state[(state == 1) & ((convolution_state == 2) | (convolution_state == 3))] = 1
    state[(state == 0) & (convolution_state == 3)] = 1
    state[(state == 0) & (convolution_state != 3)] = 0

    return state


if __name__ == "__main__":

    # Compare performance for different grid sizes
    grid_sizes = [1, 10, 20, 50, 100, 200, 500]

    np.random.seed(0)

    for grid_size in grid_sizes:
        state = np.zeros((grid_size, grid_size), dtype=int)

        for i in range(grid_size):
            for j in range(grid_size):
                state[i, j] = np.random.rand() < 0.25

        state_copy = state.copy()

        spend_time_forloop_numba_avg = life_step_for_loop_numba(state)

        state = state_copy.copy()

        spend_time_convolve_avg = life_step_convolution(state)
        print(f"About {spend_time_convolve_avg / spend_time_forloop_numba_avg:.4f}x faster")
