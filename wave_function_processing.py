import cv2
import time
import os
import os.path
import numpy as np

# GRID Parameters
GRID_PX_SIZE = 250
TILE_PX_SIZE = 50


class Tile:  # types of cells
    def __init__(self, image, edges: tuple):
        self.__image = image
        self.__edges = edges

    def __eq__(self, other):
        if np.array_equal(self.__image, other.get_image()):
            if self.__edges == other.get_edges():
                return True
        return False

    def get_image(self):
        return np.copy(self.__image)

    def get_edges(self):
        return self.__edges

    def rotate(self, num: int):
        """
        Returns tile that is rotated by 90*num degrees
        :param num: number of times to turn tile by 90 degrees
        :return: tile, rotated by 90*num degrees
        """
        num = num % len(self.__edges)
        if num == 0:
            return Tile(self.__image, self.__edges)

        rotations = [None, cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]
        image = cv2.rotate(self.__image, rotations[num])
        edges = tuple([self.__edges[(i - num) % len(self.__edges)] for i in range(len(self.__edges))])
        return Tile(image, edges)


BLANK_TILE = Tile(cv2.resize(cv2.imread('tiles/Blank.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]), (0, 0, 0, 0))
UP_TILE = Tile(cv2.resize(cv2.imread('tiles/Up.png'), dsize=[TILE_PX_SIZE, TILE_PX_SIZE]), (1, 1, 0, 1))
TILE_DICT = {"BLANK": BLANK_TILE,
             "UP": UP_TILE,
             "RIGHT": UP_TILE.rotate(1),
             "DOWN": UP_TILE.rotate(2),
             "LEFT": UP_TILE.rotate(3)}
TILE_LIST = list(TILE_DICT.values())


class Grid:

    class Cell:
        def __init__(self, collapsed, possible_states, y, x):
            self.collapsed = collapsed
            self.possible_states = possible_states
            self.y = y
            self.x = x

    def __init__(self, grid_px_size, tile_px_size, tile_list):
        self.__grid_px_size = grid_px_size
        self.__tile_px_size = tile_px_size
        assert grid_px_size >= tile_px_size, "Grid size is smaller than tile size"
        assert grid_px_size % tile_px_size == 0, "Grid must include whole number of tiles"
        self.__tiles_in_row = GRID_PX_SIZE // TILE_PX_SIZE
        self.__tiles_in_col = GRID_PX_SIZE // TILE_PX_SIZE
        self.__tile_list = tile_list
        self.__grid = np.zeros(shape=[GRID_PX_SIZE, GRID_PX_SIZE, 3], dtype=np.uint8)

        self.__cell_grid = [[self.Cell(False, self.__tile_list, j, i) for i in range(self.__tiles_in_row)]
                            for j in range(self.__tiles_in_col)]

    def get_grid(self):
        return np.copy(self.__grid)

    def set_grid(self, gr):
        self.__grid = gr

    def change_tile(self, tile: Tile, y: int, x: int) -> None:
        assert x >= 0, "x must be bigger than 0"
        assert y >= 0, "y must be bigger than 0"
        assert x < self.__tiles_in_row, "x have bigger value than possible"
        assert y < self.__tiles_in_col, "y have bigger value than possible"
        assert tile in self.__tile_list, "there is no such tile in tile list"

        # Changing cell grid
        # Updating the cell
        cell = self.__cell_grid[y][x]
        cell.collapsed = True
        cell.possible_states = [tile]

        # Updating up cell
        if y > 0:
            cell = self.__cell_grid[y - 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if tile.get_edges()[0] == pos_tile.get_edges()[2]]
        # Updating left cell
        if x > 0:
            cell = self.__cell_grid[y][x - 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if tile.get_edges()[3] == pos_tile.get_edges()[1]]
        # Updating down cell
        if y < self.__tiles_in_col - 1:
            cell = self.__cell_grid[y + 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if tile.get_edges()[2] == pos_tile.get_edges()[0]]
        # Updating right cell
        if x < self.__tiles_in_row - 1:
            cell = self.__cell_grid[y][x + 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if tile.get_edges()[1] == pos_tile.get_edges()[3]]

        # Changing grid image
        tile_arr = tile.get_image()
        self.__grid[y*self.__tile_px_size:(y+1)*self.__tile_px_size,
                    x*self.__tile_px_size:(x+1)*self.__tile_px_size, ::] = tile_arr

    def __get_non_collapsed_with_fewest_possible_states(self):
        fewest_state_cells = []
        num_fewest_state = len(self.__tile_list)
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
    grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, TILE_LIST)
    grid.change_tile(TILE_DICT["RIGHT"], 1, 0)
    grid.change_tile(TILE_DICT["UP"], 1, 2)

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
