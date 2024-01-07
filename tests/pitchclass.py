import unittest

from fractions import Fraction
from pymusictheory.core.notes import Note, PitchClass


class TestPitchClass(unittest.TestCase):

    def test_pitchclass(self):
        a4 = Note('A4')
        a4_2 = Note('A4')
        pc_a = PitchClass('A')
        pc_d = PitchClass('d')
        i = 0
        for note in pc_a:
            self.assertTrue(pc_a[i] == ''.join(('a', str(i))))
            i += 1

    def test_operator(self):
        a4 = Note('A4')
        pc_a = PitchClass('A')
        pc_b = PitchClass('b')

        self.assertTrue(a4 in pc_a)
        self.assertTrue('a4' in pc_a)
        self.assertTrue(440.0 in pc_a)
        self.assertTrue(9 in pc_a)
        self.assertFalse(a4 in pc_b)

if __name__ == '__main__':
    unittest.main()
