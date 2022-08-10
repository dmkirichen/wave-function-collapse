import os
import os.path
import cv2
import numpy as np
from tile import Tile


def compare_edges(edge1: str, edge2: str):
    return edge1.split("_") == edge2.split("_")[::-1]


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
        self.__tiles_in_row = self.__grid_px_size // self.__tile_px_size
        self.__tiles_in_col = self.__grid_px_size // self.__tile_px_size
        self.__tile_list = tile_list
        self.__grid = np.zeros(shape=[self.__grid_px_size, self.__grid_px_size, 3], dtype=np.uint8)

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
        # print(f"\nchanging possible states of neighbouring cells near ({y},{x})")
        if y > 0:
            cell = self.__cell_grid[y - 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                # print(f"({cell.y},{cell.x}):\n\tpos.states before: {[pos.get_id() for pos in cell.possible_states]}")
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if compare_edges(tile.get_edges()[0], pos_tile.get_edges()[2])]
                # print(f"\tpos.states after: {[pos.get_id() for pos in cell.possible_states]}")
        # Updating left cell
        if x > 0:
            cell = self.__cell_grid[y][x - 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                # print(f"({cell.y},{cell.x}):\n\tpos.states before: {[pos.get_id() for pos in cell.possible_states]}")
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if compare_edges(tile.get_edges()[3], pos_tile.get_edges()[1])]
                # print(f"\tpos.states after: {[pos.get_id() for pos in cell.possible_states]}")
        # Updating down cell
        if y < self.__tiles_in_col - 1:
            cell = self.__cell_grid[y + 1][x]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                # print(f"({cell.y},{cell.x}):\n\tpos.states before: {[pos.get_id() for pos in cell.possible_states]}")
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if compare_edges(tile.get_edges()[2], pos_tile.get_edges()[0])]
                # print(f"\tpos.states after: {[pos.get_id() for pos in cell.possible_states]}")
        # Updating right cell
        if x < self.__tiles_in_row - 1:
            cell = self.__cell_grid[y][x + 1]
            if not cell.collapsed:  # if state is ambiguous, update possible states
                # print(f"({cell.y},{cell.x}):\n\tpos.states before: {[pos.get_id() for pos in cell.possible_states]}")
                cell.possible_states = [pos_tile for pos_tile in cell.possible_states
                                        if compare_edges(tile.get_edges()[1], pos_tile.get_edges()[3])]
                # print(f"\tpos.states after: {[pos.get_id() for pos in cell.possible_states]}")

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
            return False  # nothing to collapse

        cell = np.random.choice(fewest_state_cells, size=1)[0]

        # Change collapsed cell on the canvas
        # print(f"cell.possible_states={cell.possible_states}")
        new_state = np.random.choice(cell.possible_states, size=1)[0]
        print(f"changing cell y={cell.y}, x={cell.x} to {new_state.get_id()} state")
        self.change_tile(new_state, cell.y, cell.x)
        return True

    def show(self):
        cv2.imshow("Grid", self.__grid)

    def save_png(self, filename: str, folder: str = "output"):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        path = os.path.join(folder, filename)
        cv2.imwrite(path, self.__grid)
