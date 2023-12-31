import unittest

from pymusictheory.definitions import *


class TestChords(unittest.TestCase):

    def test_12TET(self):
        a = 440
        c_sci = 256
        self.assertTrue(temperament['12TET'].get_note(a, 0) == a)
        self.assertTrue(temperament['12TET'].get_note(a, 12) == a*2)
        self.assertTrue(temperament['12TET'].get_note(a, -12) == a/2)
        self.assertTrue(temperament['12TET'].get_note(a, -12*4) == 27.5)
        self.assertTrue(temperament['12TET'].get_note(a, -12*4+9) == 46.25)
        self.assertTrue(temperament['12TET'].get_note(c_sci, -12*4) == 16)

    def test_temperaments(self):
        a = 440
        for (n, t) in temperament.items():
            self.assertTrue(t.get_note(a, 0) == a)
            self.assertTrue(t.get_note(a, 12) == a*2)
            self.assertTrue(t.get_note(a, -12) == a/2)
            self.assertTrue(t.get_note(a, 2*12) == a*4)


if __name__ == '__main__':
    unittest.main()
