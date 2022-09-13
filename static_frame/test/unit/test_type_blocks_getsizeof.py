import unittest
from sys import getsizeof

import numpy as np

from static_frame import TypeBlocks
from static_frame.test.test_case import TestCase


class TestUnit(TestCase):
    def test_1d_array(self) -> None:
        a = np.array([1, 2, 3])
        tb = TypeBlocks.from_blocks(a)
        self.assertTrue(getsizeof(tb), sum(getsizeof(e) for e in (
            np.array([1, 2, 3]),
            tb._blocks, # [np.array([1, 2, 3])],
            0,
            (0, 0),
            tb._index, # [(0, 0)],
            3, 1,
            tb._shape, # (3, 1),
            np.dtype('int64'),
            tb._dtypes, # [np.dtype('int64')],
            # _row_dtype, # np.dtype('int64') is already included
            None # for TypeBlocks instance garbage collector overhead
        )))

    def test_list_of_1d_arrays(self) -> None:
        tb = TypeBlocks.from_blocks([
            np.array([1, 2, 3]),
            np.array([4, 5, 6])
        ])
        self.assertEqual(getsizeof(tb), sum(getsizeof(e) for e in (
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
            tb._blocks, # [np.array([1, 2, 3]), np.array([4, 5, 6])],
            0,
            (0, 0),
            1,
            (1, 0),
            tb._index, # [(0, 0), (1, 0)],
            3, 2,
            tb._shape, # (3, 2),
            np.dtype('int64'),
            tb._dtypes, # [np.dtype('int64'), np.dtype('int64')],
            # _row_dtype, # np.dtype('int64') is already included
            None # for TypeBlocks instance garbage collector overhead
        )))

    def test_2d_array(self) -> None:
        tb = TypeBlocks.from_blocks(np.array([[1, 2, 3], [4, 5, 6]]))
        self.assertEqual(getsizeof(tb), sum(getsizeof(e) for e in (
            np.array([[1, 2, 3],[4, 5, 6]]),
            tb._blocks, # [np.array([[1, 2, 3],[4, 5, 6]])],
            0,
            (0, 0),
            1,
            (0, 1),
            2,
            (0, 2),
            tb._index, # [(0, 0), (0, 1), (0, 2)],
            3,
            tb._shape, # (2, 3),
            np.dtype('int64'),
            tb._dtypes, #[np.dtype('int64'), np.dtype('int64'), np.dtype('int64')],
            # _row_dtype, # np.dtype('int64') is already included
            None # for TypeBlocks instance garbage collector overhead
        )))

if __name__ == '__main__':
    unittest.main()