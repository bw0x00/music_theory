import unittest

from fractions import Fraction
from pymusictheory.core.intervals import Interval
from pymusictheory.core.notes import Note, PitchClass
from pymusictheory.core.chords import Chord
from pymusictheory.core.scales import Scale

class TestIntervals(unittest.TestCase):

    def test_interval_chord(self):
        c = Chord('c','powerchord')
        i = Interval('perfect_fifth')
        c2 = Chord('c', 'major')
        i2 = Interval('perfect_fifth')
        self.assertFalse(c2 == i2)

    def test_interval_scale(self):
        i = Interval('perfect_fifth')
        i2 = Interval('minor_second')

        s = Scale('c','major')

        self.assertFalse(i2 in s)
        self.assertTrue(i in s)

    def test_interval_note(self):
        i = Interval(7)
        n1 = Note('c4')
        n2 = Note('g4')
        self.assertTrue([n2,n1] == i)
        self.assertTrue((n2,n1) == i)

        self.assertFalse((n1,n2,n1) == i)
        with self.assertRaises(ValueError):
            self.assertTrue((n1,n2) == i)
        with self.assertRaises(ValueError):
            n1 - n2

        j = n2 - n1
        self.assertTrue(j.distance == 7)

        self.assertTrue(n1+i == n2)

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
