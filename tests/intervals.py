import unittest

from fractions import Fraction
from pymusictheory.core.intervals import Interval
from pymusictheory.core.notes import Note, PitchClass
from pymusictheory.core.chords import Chord

class TestIntervals(unittest.TestCase):

    def test_interval_chord(self):
        c = Chord('c','powerchord')
        i = Interval('perfect_fifth')
        self.assertTrue(c == i)

    def test_interval_note(self):
        i = Interval(7)
        n1 = Note('c4')
        n2 = Note('g4')
        self.assertTrue([n1,n2] == i)
        self.assertTrue((n1,n2) == i)
        with self.assertRaises(ValueError):
            (n1,n2,n1) == i

    def test_interval_init(self):
        i = Interval(7)
        self.assertTrue(str(i) == 'perfect_fifth')
        j = Interval('d5')
        self.assertTrue(str(j) == 'tritone')
        self.assertTrue(j.distance == 6)
        self.assertTrue(j.name == 'tritone' )
        self.assertTrue(j.short_names == ['d5', 'A4'])
        k = Interval('semitone')
        self.assertTrue(k.short_names == ['m2', 'A1'])
        self.assertTrue(k.short_names == ['m2', 'A1'])
        self.assertTrue(str(k) == 'minor_second')
        self.assertTrue(k.distance == 1)
        with self.assertRaises(ValueError):
            Interval(5.0)

if __name__ == '__main__':
    unittest.main()
