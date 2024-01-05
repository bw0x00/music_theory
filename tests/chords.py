import unittest

from fractions import Fraction
from pymusictheory.core.chords import Chord
from pymusictheory.core.notes import Note, PitchClass

class TestChords(unittest.TestCase):

    def test_chord(self):
        Cmaj = ['c4',  'e4',  'g4']
        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_chord() == Cmaj)

    def test_chord_composition(self):
        Cmaj = ['c4', 'e4', 'g4' ]
        s = Chord(root='c', chord='powerchord')
        s2 = s + PitchClass('e')
        self.assertTrue(s2.get_chord() == Cmaj)


    def test_chord_frequencies(self):
        Cmaj = [261.63, 329.63, 392.0]
        Cmaj7 = [261.63, 329.63, 392.0, 493.88]

        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_frequencies() == Cmaj)
        s = Chord(root='c', chord='major7')
        self.assertTrue(s.get_frequencies() == Cmaj7)



if __name__ == '__main__':
    unittest.main()
