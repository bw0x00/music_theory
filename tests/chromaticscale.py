import unittest

from pymusictheory.scales import ChromaticScale
from fractions import Fraction


class TestChromaticScale(unittest.TestCase):

    def testSCIScale(self):
        sci = ChromaticScale(note=('c3', 256))
        self.assertTrue(round(sci.get_octaves()[0][0],2) == 26.91)
        self.assertTrue(sci.get_octaves()[3][3] == 256.0)

    def testStandardScale(self):
        sc = ChromaticScale(note=('a4', 440))
        self.assertTrue(sc.get_octaves()[0][0] == 27.5)
        self.assertTrue(sc.get_octaves()[4][0] == 440)
        self.assertTrue(sc.get_octaves()[1][10] == 98.0)


if __name__ == '__main__':
    unittest.main()
