import unittest
import numpy as np
from wave_function_processing import Tile


class TestTileClass(unittest.TestCase):
    def setUp(self):
        self.tile = Tile(np.array([[0, 1], [2, 3]]), (1, 2, 3, 4))

    def test_one_rotation(self):
        rot_tile = Tile(np.array([[2, 0], [3, 1]]), (4, 1, 2, 3))
        res = self.tile.rotate(1)

        self.assertTrue(np.array_equal(res.get_image(), rot_tile.get_image()), "incorrect rotation (image is wrong)")
        self.assertEqual(res.get_edges(), rot_tile.get_edges(), "incorrect rotation (edges are wrong)")

    def test_two_rotations(self):
        rot_tile = Tile(np.array([[3, 2], [1, 0]]), (3, 4, 1, 2))
        res = self.tile.rotate(2)

        self.assertTrue(np.array_equal(res.get_image(), rot_tile.get_image()), "incorrect rotation (image is wrong)")
        self.assertEqual(res.get_edges(), rot_tile.get_edges(), "incorrect rotation (edges are wrong)")

    def test_four_rotations(self):
        rot_tile = Tile(np.array([[0, 1], [2, 3]]), (1, 2, 3, 4))
        res = self.tile.rotate(4)

        self.assertTrue(np.array_equal(res.get_image(), rot_tile.get_image()), "incorrect rotation (image is wrong)")
        self.assertEqual(res.get_edges(), rot_tile.get_edges(), "incorrect rotation (edges are wrong)")


if __name__ == "__main__":
    unittest.main()
