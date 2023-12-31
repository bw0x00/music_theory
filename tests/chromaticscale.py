import unittest

from pymusictheory.scales import ChromaticScale
from fractions import Fraction


class TestChromaticScale(unittest.TestCase):

    def test_sci_scale(self):
        sci = ChromaticScale(note=('c4', 256))
        self.assertTrue(sci.get_octaves()[0][0] == 16.0)
        self.assertTrue(sci.get_octaves()[4][0] == 256.0)
        self.assertTrue(round(sci.get_octaves()[0][9],2) == 26.91)

    def test_standard_scale(self):
        sc = ChromaticScale(note=('a4', 440))
        self.assertTrue(sc.get_octaves()[0][9] == 27.5)
        self.assertTrue(sc.get_octaves()[4][9] == 440)
        self.assertTrue(sc.get_octaves()[2][7] == 98.0)


if __name__ == '__main__':
    unittest.main()
