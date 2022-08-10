import os.path
import cv2
import time
from grid import Grid
from utils import load_tiles_config

# Possible options
GRID_PX_SIZE = 500
TILE_PX_SIZE = 25
TILES_FOLDER = "tiles/circuit_board"

# Reading config about tiles info
config_path = os.path.join(TILES_FOLDER, "tiles.json")
TILE_LIST = load_tiles_config(config_path, TILE_PX_SIZE, tiles_folder=TILES_FOLDER)

if __name__ == "__main__":
    while True:  # restarting each failed attempt
        grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, TILE_LIST)
        grid.show()

        # key = cv2.waitKey(0)
        # if key == ord('n'):
        #     # next iteration
        #     print("next iteration")
        # elif key == ord('s'):
        #     print("attempt to save the image")
        #     name = f"grid_{int(time.time())}.png"
        #     grid.save_png(name)
        #     break
        # else:
        #     break
        try:
            while True:
                ret = grid.collapse_next_cell()
                grid.show()
                cv2.waitKey(25)
                if not ret:
                    name = f"grid_{int(time.time())}.png"
                    grid.save_png(name)
                    cv2.waitKey(0)
                    exit(0)
        except ValueError:
            continue

    cv2.destroyAllWindows()
