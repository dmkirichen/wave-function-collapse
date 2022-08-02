import cv2
import time
import os
import os.path
import numpy as np

# GRID Parameters
GRID_PX_SIZE = 250
TILE_PX_SIZE = 50

# Loading tiles as numpy arrays
IMAGE_DICT = {"BLANK": cv2.resize(cv2.imread('tiles/blank.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]),
              "UP":    cv2.resize(cv2.imread('tiles/up.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]),
              "LEFT":  cv2.resize(cv2.imread('tiles/left.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]),
              "RIGHT": cv2.resize(cv2.imread('tiles/right.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]),
              "DOWN":  cv2.resize(cv2.imread('tiles/down.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE])}
NEIGHBOURS_DICT = {"UP":    {"up":    ["DOWN", "LEFT", "RIGHT"],
                             "right": ["DOWN", "LEFT", "UP"],
                             "down":  ["BLANK", "DOWN"],
                             "left":  ["DOWN", "RIGHT", "UP"]},

                   "RIGHT": {"up":    ["DOWN", "LEFT", "RIGHT"],
                             "right": ["DOWN", "LEFT", "UP"],
                             "down":  ["LEFT", "RIGHT", "UP"],
                             "left":  ["BLANK", "LEFT"]},

                   "DOWN":  {"up":    ["BLANK", "UP"],
                             "right": ["DOWN", "LEFT", "UP"],
                             "down":  ["LEFT", "RIGHT", "UP"],
                             "left":  ["DOWN", "RIGHT", "UP"]},

                   "LEFT":  {"up":    ["DOWN", "LEFT", "RIGHT"],
                             "right": ["BLANK", "RIGHT"],
                             "down":  ["LEFT", "RIGHT", "UP"],
                             "left":  ["DOWN", "RIGHT", "UP"]},

                   "BLANK": {"up":    ["BLANK", "UP"],
                             "right": ["BLANK", "RIGHT"],
                             "down":  ["BLANK", "DOWN"],
                             "left":  ["BLANK", "LEFT"]}}


class Grid:

    class Cell:
        def __init__(self, collapsed, possible_states, y, x):
            self.collapsed = collapsed
            self.possible_states = possible_states
            self.y = y
            self.x = x

    def __init__(self, grid_px_size, tile_px_size, image_dict, neighbours_dict):
        self.__grid_px_size = grid_px_size
        self.__tile_px_size = tile_px_size
        assert grid_px_size >= tile_px_size, "Grid size is smaller than tile size"
        assert grid_px_size % tile_px_size == 0, "Grid must include whole number of tiles"
        self.__tiles_in_row = GRID_PX_SIZE // TILE_PX_SIZE
        self.__tiles_in_col = GRID_PX_SIZE // TILE_PX_SIZE
        self.__image_dict = image_dict
        self.__neighbours_dict = neighbours_dict
        self.__grid = np.zeros(shape=[GRID_PX_SIZE, GRID_PX_SIZE, 3], dtype=np.uint8)

        self.__cell_grid = [[self.Cell(False, list(self.__image_dict.keys()), j, i) for i in range(self.__tiles_in_row)]
                            for j in range(self.__tiles_in_col)]

    def get_grid(self):
        return self.__grid

    def set_grid(self, gr):
        self.__grid = gr

    def change_tile(self, tile_str: str, y: int, x: int) -> None:
        assert x >= 0, "x must be bigger than 0"
        assert y >= 0, "y must be bigger than 0"
        assert x < self.__tiles_in_row, "x have bigger value than possible"
        assert y < self.__tiles_in_col, "y have bigger value than possible"
        assert tile_str in self.__image_dict, "there is no such key in tile dict"

        # Changing cell grid
        # Updating the cell
        cell = self.__cell_grid[y][x]
        cell.collapsed = True
        cell.possible_states = [tile_str]

        # Updating up cell
        if y > 0:
            cell = self.__cell_grid[y - 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [state for state in cell.possible_states
                                        if state in self.__neighbours_dict[tile_str]["up"]]
        # Updating left cell
        if x > 0:
            cell = self.__cell_grid[y][x - 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [state for state in cell.possible_states
                                        if state in self.__neighbours_dict[tile_str]["left"]]
        # Updating down cell
        if y < self.__tiles_in_col - 1:
            cell = self.__cell_grid[y + 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [state for state in cell.possible_states
                                        if state in self.__neighbours_dict[tile_str]["down"]]
        # Updating right cell
        if x < self.__tiles_in_row - 1:
            cell = self.__cell_grid[y][x + 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [state for state in cell.possible_states
                                        if state in self.__neighbours_dict[tile_str]["right"]]

        # Changing grid image
        tile_arr = self.__image_dict[tile_str]
        self.__grid[y*self.__tile_px_size:(y+1)*self.__tile_px_size,
                    x*self.__tile_px_size:(x+1)*self.__tile_px_size, ::] = tile_arr

    def __get_non_collapsed_with_fewest_possible_states(self):
        fewest_state_cells = []
        num_fewest_state = len(self.__image_dict.keys())
        is_there_non_collapsed = False
        for row in self.__cell_grid:
            for cell in row:
                if not cell.collapsed:
                    is_there_non_collapsed = True
                    if len(cell.possible_states) == num_fewest_state:
                        fewest_state_cells.append(cell)
                    elif len(cell.possible_states) < num_fewest_state:
                        fewest_state_cells = [cell]
                        num_fewest_state = len(cell.possible_states)
        if not is_there_non_collapsed:
            return []
        return fewest_state_cells

    def collapse_next_cell(self):
        # Choose cell to collapse
        fewest_state_cells = self.__get_non_collapsed_with_fewest_possible_states()
        if len(fewest_state_cells) == 0:
            return  # nothing to collapse

        cell = np.random.choice(fewest_state_cells, size=1)[0]

        # Change collapsed cell on the canvas
        # print(f"cell.possible_states={cell.possible_states}")
        new_state = np.random.choice(cell.possible_states, size=1)[0]
        print(f"changing cell y={cell.y}, x={cell.x} to {new_state} state")
        self.change_tile(new_state, cell.y, cell.x)

    def show(self):
        cv2.imshow("Grid", self.__grid)

    def save_png(self, filename: str, folder: str = "output"):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        path = os.path.join(folder, filename)
        cv2.imwrite(path, self.__grid)


if __name__ == "__main__":
    grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, IMAGE_DICT, NEIGHBOURS_DICT)
    grid.change_tile("RIGHT", 1, 0)
    grid.change_tile("UP", 1, 2)

    grid.show()

    while True:
        key = cv2.waitKey(0)
        if key == ord('n'):
            # next iteration
            print("next iteration")
        elif key == ord('s'):
            print("attempt to save the image")
            name = f"grid_{int(time.time())}.png"
            grid.save_png(name)
            break
        else:
            break
        grid.collapse_next_cell()
        grid.show()

    cv2.destroyAllWindows()
