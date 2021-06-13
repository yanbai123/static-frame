

import unittest

import frame_fixtures as ff
# import numpy as np

# from static_frame import Frame
# from static_frame import Series
from static_frame.test.test_case import TestCase


class TestUnit(TestCase):

    def test_frame_via_re_a(self) -> None:
        f1 = ff.parse('s(3,3)|c(I,str)|i(I,str)|v(int)')

        self.assertEqual(
            f1.via_re('8[68]').search().to_pairs(),
            (('zZbu', (('zZbu', True), ('ztsv', True), ('zUvW', False))), ('ztsv', (('zZbu', False), ('ztsv', False), ('zUvW', False))), ('zUvW', (('zZbu', False), ('ztsv', False), ('zUvW', False))))
            )

        self.assertEqual(
            f1.via_re('9').search(endpos=2).to_pairs(),
            (('zZbu', (('zZbu', False), ('ztsv', True), ('zUvW', False))), ('ztsv', (('zZbu', False), ('ztsv', False), ('zUvW', False))), ('zUvW', (('zZbu', False), ('ztsv', True), ('zUvW', False))))
            )

    def test_frame_via_re_b(self) -> None:
        f1 = ff.parse('s(2,5)|c(I,str)|i(I,str)|v(int,bool,bool,float,str)')

        self.assertEqual(
            f1.via_re('[a.-]').search().to_pairs(),
                (('zZbu', (('zZbu', True), ('ztsv', False))), ('ztsv', (('zZbu', True), ('ztsv', True))), ('zUvW', (('zZbu', False), ('ztsv', True))), ('zkuW', (('zZbu', True), ('ztsv', True))), ('zmVj', (('zZbu', False), ('ztsv', False))))
            )

        import re

        self.assertEqual(
            f1.via_re('f', re.I).match(endpos=2).to_pairs(),
            (('zZbu', (('zZbu', False), ('ztsv', False))), ('ztsv', (('zZbu', True), ('ztsv', True))), ('zUvW', (('zZbu', False), ('ztsv', True))), ('zkuW', (('zZbu', False), ('ztsv', False))), ('zmVj', (('zZbu', False), ('ztsv', False))))
            )

        self.assertEqual(
            f1.via_re('z[5h][5h]i', re.I).fullmatch().to_pairs(),
            (('zZbu', (('zZbu', False), ('ztsv', False))), ('ztsv', (('zZbu', False), ('ztsv', False))), ('zUvW', (('zZbu', False), ('ztsv', False))), ('zkuW', (('zZbu', False), ('ztsv', False))), ('zmVj', (('zZbu', False), ('ztsv', True)))))

    def test_frame_via_re_c(self) -> None:
        f1 = ff.parse('s(2,5)|c(I,str)|i(I,str)|v(int,bool,bool,float,str)')

        self.assertEqual(f1.via_re('[a.r]').split().to_pairs(),
            (('zZbu', (('zZbu', ('-88017',)), ('ztsv', ('92867',)))), ('ztsv', (('zZbu', ('F', 'lse')), ('ztsv', ('F', 'lse')))), ('zUvW', (('zZbu', ('T', 'ue')), ('ztsv', ('F', 'lse')))), ('zkuW', (('zZbu', ('1080', '4')), ('ztsv', ('2580', '34')))), ('zmVj', (('zZbu', ('zDVQ',)), ('ztsv', ('z5hI',)))))
            )
        # import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    unittest.main()
