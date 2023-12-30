import unittest

from fractions import Fraction
from pymusictheory.chords import Chord


class TestChords(unittest.TestCase):

    def testChord(self):
        Cmaj = [['c'],  ['e'],  ['g']]
        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_chord() == Cmaj)

    def testChordFrequencies(self):
        Cmaj = [261.63, 329.63, 392.0] 
        s = Chord(root='c', chord='major')
        self.assertTrue(s.get_frequencies() == Cmaj)


if __name__ == '__main__':
    unittest.main()
