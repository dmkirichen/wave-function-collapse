import unittest
import numpy as np
from tile import Tile
from grid import compare_edges, Grid


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


class TestGridClass(unittest.TestCase):
    # def setUp(self):
    #     tile1 = Tile(np.array([[0, 1], [2, 3]]), ("A_A_A", "A_A_B", "A_A_A", "B_A_A"))
    #     tile2 = Tile(np.array([[4, 5], [6, 7]]), ("A_A_A", "A_A_A", "A_A_A", "A_A_A"))
    #     self.grid = Grid(20, 10, [tile1,
    #                               tile2])
    #     self.grid.change_tile(tile1, 0, 0)

    def test_compare_edges(self):
        self.assertTrue(compare_edges("A_B_C", "C_B_A"), "edges are not connected properly")


if __name__ == "__main__":
    unittest.main()
