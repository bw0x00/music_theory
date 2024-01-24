import unittest

from fractions import Fraction
from trallala.core.temperament import _CoreChromaticScale


class TestCoreChromaticScale(unittest.TestCase):

    def test_sci_scale(self):
        sci = _CoreChromaticScale(note=('c4', 256))
        self.assertTrue(sci.get_octaves()[0][0] == 16.0)
        self.assertTrue(sci.get_octaves()[4][0] == 256.0)
        self.assertTrue(round(sci.get_octaves()[0][9],2) == 26.91)

    def test_standard_scale(self):
        sc = _CoreChromaticScale(note=('a4', 440))
        self.assertTrue(sc.get_octaves()[0][9] == 27.5)
        self.assertTrue(sc.get_octaves()[4][9] == 440)
        self.assertTrue(sc.get_octaves()[2][7] == 98.0)

    def test_conversion(self):
        sc = _CoreChromaticScale(note=('a4', 440))
        dist = sc.spn_to_distance('a4')
        self.assertTrue( sc.frequencyof(dist) == 440)
        self.assertTrue( sc.frequencyof(2*12+7) == 98.0)
        self.assertTrue( sc.spn_from_distance(dist) == 'a4')


if __name__ == '__main__':
    unittest.main()
