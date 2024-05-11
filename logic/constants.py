CELL_SIZE = 25
FPS = 12
RANDOM_RATIO = 0.25

INIT_DRAW_WIDTH = 800
INIT_DRAW_HEIGHT = 800

COLOR_ALIVE = "#227722"
COLOR_DEAD = "#222222"
COLOR_TAIL = "#444444"
COLOR_SURFACE = "#bbbbbb"


class Flag:
    class Grid:
        survival_world_border = 2 ** 0
        survival_world_donut = 2 ** 1
        show_tail = 2 ** 2
        show_traces_of_death = 2 ** 3
