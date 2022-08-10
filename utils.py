import cv2
import json
import os.path
from tile import Tile


def load_tiles_config(config_path: str, tile_px_size, tiles_folder=".") -> list:
    with open(config_path) as f:
        tiles_info = json.load(f)

    tile_list = []
    for tile_info in tiles_info["tiles"]:
        path = os.path.join(tiles_folder, tile_info["filename"])
        assert os.path.exists(path), f"{path} does not exist in the system"
        image = cv2.resize(cv2.imread(path), dsize=[tile_px_size, tile_px_size])
        edges = tuple(tile_info["edges"])
        new_tile = Tile(image, edges, tile_id=tile_info["filename"])
        tile_list.append(new_tile)
        for rotation in tile_info["rotations"]:
            tile_list.append(new_tile.rotate(rotation))
    return tile_list
