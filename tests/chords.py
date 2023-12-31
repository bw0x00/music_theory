import unittest

from fractions import Fraction
from pymusictheory.chords import Chord


class TestChords(unittest.TestCase):

    def test_chord(self):
        Cmaj = [['c'],  ['e'],  ['g']]
        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_chord() == Cmaj)

    def test_chord_frequencies(self):
        Cmaj = [261.63, 329.63, 392.0]
        Cmaj7 = [261.63, 329.63, 392.0, 493.88]

        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_frequencies() == Cmaj)
        s = Chord(root='c', chord='major7')
        self.assertTrue(s.get_frequencies() == Cmaj7)



if __name__ == '__main__':
    unittest.main()
