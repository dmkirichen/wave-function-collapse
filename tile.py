import cv2
import numpy as np


class Tile:  # types of cells
    def __init__(self, image, edges: tuple, tile_id=None):
        self.__id = tile_id
        self.__image = image
        self.__edges = edges

    def __eq__(self, other):
        if np.array_equal(self.__image, other.get_image()):
            if self.__edges == other.get_edges():
                return True
        return False

    def get_id(self):
        return self.__id

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
        tile_id = f"{self.__id}_rot{num}" if self.__id is not None else None
        return Tile(image, edges, tile_id=tile_id)
