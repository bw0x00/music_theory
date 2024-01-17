import unittest

from fractions import Fraction
from trallala.core.scales import Scale
from trallala.core.notes import PitchClass

class TestScale(unittest.TestCase):

    def test_init(self):
        s = Scale(root='c', scale='major')
        pc = PitchClass('c')
        s2 = Scale(root=pc)

    def test_cmaj(self):
        Cmaj = [['c'], ['d'], ['e'], ['f'], ['g'], ['a'], ['b']]
        s = Scale(root='c', scale='major')
        self.assertTrue(s.get_scale() == Cmaj)
        self.assertTrue(s.get_scale_frequencies(4)[5] == 440.0)

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
