import unittest

from fractions import Fraction
from pymusictheory.scales import Scale


class TestScale(unittest.TestCase):

    def test_cmaj(self):
        Cmaj = [['c'], ['d'], ['e'], ['f'], ['g'], ['a'], ['b']]
        s = Scale(root='c', scale='major')
        self.assertTrue(s.get_scale() == Cmaj)

    def test_amin(self):
        Amin = [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g']]
        s = Scale(root='a', scale='minor')
        self.assertTrue(s.get_scale() == Amin)

    def test_csharpmin(self):
        Csharpmin = [['c#', 'db'], ['d#', 'eb'], ['e'],
                     ['f#', 'gb'], ['g#', 'ab'], ['a'], ['b']]
        s = Scale(root='c#', scale='minor')
        self.assertTrue(s.get_scale() == Csharpmin)


if __name__ == '__main__':
    unittest.main()