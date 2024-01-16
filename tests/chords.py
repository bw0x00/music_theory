import unittest

from pymusictheory.core.chords import Chord
from pymusictheory.core.notes import Note, PitchClass
from pymusictheory.core.intervals import Interval
from pymusictheory.core.scales import Scale

class TestChords(unittest.TestCase):

    def test_chord_init(self):
        Cmaj = ['c4',  'e4',  'g4']
        s = Chord('major', root='c')
        self.assertTrue(s.get_chord() == Cmaj)

        C5 = ['c4', 'g4']
        self.assertTrue(s == s)
        self.assertFalse(C5 == s.get_chord())

        Cmaj2 = ['c3', 'e3', 'g4']
        self.assertFalse(s.get_chord() == Cmaj2)
        s.voicing = (3,3,4)
        self.assertTrue(s.get_chord() == Cmaj2)

        i_cmaj = (Interval('perfect_unison'),
                  Interval('major_third'),
                  Interval('perfect_fifth')
                )
        s_i = Chord(i_cmaj, root='c')
        self.assertTrue(s_i == i_cmaj)
        self.assertTrue(s_i == Cmaj)

    def test_chord_composition(self):
        Cmaj = ['c4', 'e4', 'g4' ]
        s = Chord('powerchord', root='c')
        s2 = s + PitchClass('e')
        with self.assertRaises(ValueError):
            s3 = s + Note('e4')
        s.voicing = (4, 4)
        s3 = s + Note('e4')
        self.assertTrue(s2.get_chord() == Cmaj)
        self.assertTrue(s3.get_chord() == Cmaj)

        self.assertTrue(s2.get_pitchclasses() == tuple([PitchClass(n) for n in Cmaj]))

        i = Interval(4)
        i2 = Interval(7)
        s4 = s + i
        self.assertTrue(s4.get_chord() == Cmaj)
        s5 = s + i2
        self.assertTrue(s5 == s)

    def test_chord_frequencies(self):
        Cmaj = [261.63, 329.63, 392.0]
        Cmaj7 = [261.63, 329.63, 392.0, 493.88]

        s = Chord('major', root='c')
        self.assertTrue(s.get_frequencies() == Cmaj)
        s = Chord('major7', root='c')
        self.assertTrue(s.get_frequencies() == Cmaj7)

    def test_chord_operators(self):
        c = Chord('major', root='c')
        self.assertTrue(c[0] == Note('c4'))

    def test_chord_contains(self):
        pc = PitchClass('e')
        i = Interval(7)
        n = Note('g4')
        Cmaj = [261.63, 329.63, 392.0]
        s = Chord('major', root='c')

        self.assertTrue(pc in s)
        self.assertTrue(i in s)

        with self.assertRaises(ValueError):
            self.assertTrue(Cmaj[0] in s)
        with self.assertRaises(ValueError):
            self.assertTrue(n in s)

        s.voicing = [4,4,4]
        self.assertTrue(Cmaj[0] in s)
        self.assertTrue(n in s)

    def test_chord_scale(self):
        scale = Scale('c')
        c4 = Chord('major',root='c')

        self.assertTrue(c4 in scale)
        # vocing doesn't matter
        c4.voicing = (4,4,4)
        self.assertTrue(c4 in scale)

if __name__ == '__main__':
    unittest.main()
