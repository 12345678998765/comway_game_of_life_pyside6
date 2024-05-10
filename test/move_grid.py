import numpy as np

size = 10

cells = np.arange(1, size * size + 1).reshape(size, size)

grid1_TopLeft = (0, 0)
grid1_BottomRight = (size, size)

grid2_TopLeft = (0, 0)
grid2_BottomRight = (size, size)


def get_vectors(delta_row, delta_col):
    grid_move_vector = (delta_row, delta_col)
    locate_start_location_vector = (-delta_row, -delta_col)
    return grid_move_vector, locate_start_location_vector


def get_last_synthesized_grid_move_vector(grid_1, grid_2):
    grid1_TopLeft, grid1_BottomRight = grid_1  # screen
    grid2_TopLeft, grid2_BottomRight = grid_2  # overlapped
    size = grid1_BottomRight[0] - grid1_TopLeft[0]

    abs_delta_row = (grid1_BottomRight[0] - grid1_TopLeft[0]) - (grid2_BottomRight[0] - grid2_TopLeft[0])
    abs_delta_col = (grid1_BottomRight[1] - grid1_TopLeft[1]) - (grid2_BottomRight[1] - grid2_TopLeft[1])

    if grid2_TopLeft == (0, 0) and grid2_BottomRight == (size, size):
        return abs_delta_row, abs_delta_col
    elif grid2_TopLeft == (0, 0) and grid2_BottomRight != (size, size):
        return -abs_delta_row, -abs_delta_col
    elif grid2_TopLeft != (0, 0) and grid2_BottomRight == (size, size):
        return abs_delta_row, abs_delta_col
    elif grid2_TopLeft[0] > 0 and grid2_BottomRight[1] < size:
        return -abs_delta_row, abs_delta_col
    elif grid2_TopLeft[1] > 0 and grid2_BottomRight[0] < size:
        return abs_delta_row, -abs_delta_col
    else:
        raise ValueError("Invalid grid move vector.")


def move_grid(grid_move_vector, origin_grid_TopLeft, origin_grid_BottomRight):
    last_synthesized_grid_move_vector = get_last_synthesized_grid_move_vector((grid1_TopLeft, grid1_BottomRight), (grid2_TopLeft, grid2_BottomRight))
    new_grid_move_vector = last_synthesized_grid_move_vector[0] + grid_move_vector[0], last_synthesized_grid_move_vector[1] + grid_move_vector[1]

    new_grid_TopLeft = (max(0, origin_grid_TopLeft[0] + new_grid_move_vector[0]), max(0, origin_grid_TopLeft[1] + new_grid_move_vector[1]))
    new_grid_BottomRight = (min(size - 1, origin_grid_BottomRight[0] + new_grid_move_vector[0]), min(size - 1, origin_grid_BottomRight[1] + new_grid_move_vector[1]))
    return new_grid_TopLeft, new_grid_BottomRight, new_grid_move_vector


def print_grid(grid_TopLeft, grid_BottomRight, locate_start_location_vector):
    for row in range(grid_TopLeft[0], grid_BottomRight[0]):
        for col in range(grid_TopLeft[1], grid_BottomRight[1]):
            print(cells[row + locate_start_location_vector[0]][col + locate_start_location_vector[1]], end=" ")
        print()


if __name__ == "__main__":
    print(cells)

    delta_row, delta_col = -3, -4
    grid_move_vector, locate_start_location_vector = get_vectors(delta_row, delta_col)
    grid2_TopLeft, grid2_BottomRight, grid_move_vector = move_grid(grid_move_vector, grid1_TopLeft, grid1_BottomRight)
    print(grid2_TopLeft, grid2_BottomRight)
    print_grid(grid2_TopLeft, grid2_BottomRight, locate_start_location_vector)

    delta_row, delta_col = 1, 2
    grid_move_vector, locate_start_location_vector = get_vectors(delta_row, delta_col)
    grid2_TopLeft, grid2_BottomRight, grid_move_vector = move_grid(grid_move_vector, grid1_TopLeft, grid1_BottomRight)
    grid_move_vector, locate_start_location_vector = get_vectors(grid_move_vector[0], grid_move_vector[1])
    print(grid2_TopLeft, grid2_BottomRight)
    print_grid(grid2_TopLeft, grid2_BottomRight, locate_start_location_vector)

    delta_row, delta_col = 3, 4
    grid_move_vector, locate_start_location_vector = get_vectors(delta_row, delta_col)
    grid2_TopLeft, grid2_BottomRight, grid_move_vector = move_grid(grid_move_vector, grid1_TopLeft, grid1_BottomRight)
    grid_move_vector, locate_start_location_vector = get_vectors(grid_move_vector[0], grid_move_vector[1])
    print(grid2_TopLeft, grid2_BottomRight)
    print_grid(grid2_TopLeft, grid2_BottomRight, locate_start_location_vector)
