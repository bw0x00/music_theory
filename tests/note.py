import unittest

from fractions import Fraction
from pymusictheory.notes import Note, PitchClass


class TestChords(unittest.TestCase):

    def test_init(self):
        a4 = Note('A4')
        a4_2 = Note(a4)
        a4_3 = Note(440.0)
        a4_4 = Note(12*4+3)

    def test_compare(self):
        a4 = Note('A4')
        a4_2 = Note('A4')
        pc_a = PitchClass('A')
        pc_d = PitchClass('d')
        self.assertTrue( a4 == 'A4')
        self.assertTrue( a4_2 == 'A4')
        self.assertTrue( a4 != 'C4')
        self.assertTrue( a4 == 440)
        self.assertTrue( a4 < 'A#4')
        self.assertTrue( a4 > 'Ab4')
        self.assertTrue( a4 in pc_a)
        self.assertTrue( a4 not in pc_d)

    def test_math_opertor(self):
        a4 = Note('A4')
        self.assertTrue( a4+12 == a4*2 )
        self.assertTrue( a4+2*12 == a4*2*2 )
        self.assertTrue( a4/(2**4) == 'A0' )

    def test_pitchclass(self):
        a4 = Note('A4')
        a4_2 = Note('A4')
        pc_a = PitchClass('A')
        pc_d = PitchClass('d')
        i = 0
        for note in pc_a:
            self.assertTrue(pc_a[i] == ''.join(('a',str(i))) )
            i += 1

if __name__ == '__main__':
    unittest.main()
