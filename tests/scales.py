import unittest

from fractions import Fraction
from pymusictheory.core.scales import Scale
from pymusictheory.core.notes import PitchClass

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

    def test_operator(self):
        s = Scale(root='c#', scale='minor')
        self.assertTrue(PitchClass('c#') in s)
        self.assertFalse(PitchClass('c') in s)


if __name__ == '__main__':
    unittest.main()
