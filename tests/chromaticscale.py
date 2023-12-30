import unittest

from pymusictheory.scales import ChromaticScale
from fractions import Fraction


class TestChromaticScale(unittest.TestCase):

    def testSCIScale(self):
        sci = ChromaticScale(note=('c3', 256))
        self.assertTrue(sci.get_octaves()[0][0] == Fraction(128, 5))
        self.assertTrue(sci.get_octaves()[3][3] == 256)

    def testStandardScale(self):
        sci = ChromaticScale(note=('a4', 440))
        self.assertTrue(sci.get_octaves()[0][0] == 27.5)
        self.assertTrue(sci.get_octaves()[4][0] == 440)


if __name__ == '__main__':
    unittest.main()
