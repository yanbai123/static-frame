

import unittest

import frame_fixtures as ff

from static_frame import Frame
from static_frame.core.index import ILoc
from static_frame.test.test_case import TestCase


class TestUnit(TestCase):

    def test_frame_via_fill_value_a(self) -> None:

        f1 = ff.parse('s(3,3)|c(I,str)|i(I,str)|v(int)')
        f2 = ff.parse('s(2,2)|c(I,str)|i(I,str)|v(int)')

        f3 = f1.via_fill_value(0) + f2
        self.assertEqual(f3.to_pairs(),
                (('zUvW', (('zUvW', 30205), ('zZbu', -3648), ('ztsv', 91301))), ('zZbu', (('zUvW', 84967), ('zZbu', -176034), ('ztsv', 185734))), ('ztsv', (('zUvW', 5729), ('zZbu', 324394), ('ztsv', -82314))))
                )


        f4 = f1.via_fill_value(0) + f2.iloc[0]
        self.assertEqual(f4.to_pairs(),
                (('zUvW', (('zZbu', -3648), ('ztsv', 91301), ('zUvW', 30205))), ('zZbu', (('zZbu', -176034), ('ztsv', 4850), ('zUvW', -3050))), ('ztsv', (('zZbu', 324394), ('ztsv', 121040), ('zUvW', 167926))))
                )


    def test_frame_via_fill_value_b(self) -> None:

        f1 = ff.parse('s(3,3)|c(I,str)|i(I,str)|v(int)')
        f2 = ff.parse('s(2,2)|c(I,str)|i(I,int)|v(int)') % 3

        f3 =  f1.via_T.via_fill_value(1) * f2.iloc[0]

        self.assertEqual(f3.to_pairs(),
                (('zZbu', (('zUvW', 84967), ('zZbu', 0), ('ztsv', 185734))), ('ztsv', (('zUvW', 5729), ('zZbu', 0), ('ztsv', -82314))), ('zUvW', (('zUvW', 30205), ('zZbu', 0), ('ztsv', 182602))))
                )

        f4 =  f1.via_fill_value(1).via_T * f2.iloc[0]

        self.assertEqual(f4.to_pairs(),
                (('zZbu', (('zUvW', 84967), ('zZbu', 0), ('ztsv', 185734))), ('ztsv', (('zUvW', 5729), ('zZbu', 0), ('ztsv', -82314))), ('zUvW', (('zUvW', 30205), ('zZbu', 0), ('ztsv', 182602))))
                )



if __name__ == '__main__':
    unittest.main()
