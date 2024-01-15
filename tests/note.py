import unittest

from fractions import Fraction
from pymusictheory.core.notes import Note, PitchClass
from pymusictheory.core.scales import ChromaticScale

class TestNotes(unittest.TestCase):

    def test_init(self):
        a4 = Note('A4')
        a4_2 = Note(a4)
        a4_3 = Note(440.0)
        a4_4 = Note(12*4+9)
        a4 = Note('a4', ChromaticScale(('a4',44)))
        self.assertTrue('a4' == a4)
        self.assertTrue('a4' == a4_2)
        self.assertTrue('a4' == a4_3)
        self.assertTrue('a4' == a4_4)

    def test_compare(self):
        a4 = Note('A4')
        a4_2 = Note('A4')
        pc_a = PitchClass('A')
        pc_d = PitchClass('d')
        self.assertTrue(a4 == 'A4')
        self.assertTrue(a4_2 == 'A4')
        self.assertTrue(a4 != 'C4')
        self.assertTrue(a4 == 440)
        self.assertTrue(a4 < 'A#4')
        self.assertTrue(a4 <= 'A#4')
        self.assertTrue(a4 <= 'A4')
        self.assertTrue(a4 > 'Ab4')
        self.assertTrue(a4 >= 'Ab4')
        self.assertTrue(a4 >= 'A4')
        self.assertTrue(a4 in pc_a)
        self.assertTrue(a4 not in pc_d)

    def test_math_opertor(self):
        a4 = Note('A4')
        self.assertTrue(a4+12 == a4*2)
        self.assertTrue(a4+2*12 == a4*2*2)
        with self.assertRaises(TypeError):
            4/a4
        with self.assertRaises(ValueError):
            a4/0
        self.assertTrue(a4/5 == 'A0')
        self.assertTrue(a4/2 == a4*0.5)
        self.assertTrue(a4/0.5 == a4*2)


if __name__ == '__main__':
    unittest.main()
