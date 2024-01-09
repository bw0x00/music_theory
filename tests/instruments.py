import unittest

from fractions import Fraction
from pymusictheory.core.scales import Scale
from pymusictheory.core.notes import PitchClass, Note
from pymusictheory.instruments.coreinstruments import _Instrument, _StringedInstrument

class TestInstrument(unittest.TestCase):

    def test_init_instrument(self):
        n1 = Note('e2')
        n2 = Note('e6')
        i = _Instrument(n1,n2)

        self.assertTrue( i.lowest_note == n1)
        self.assertTrue( i.highest_note == n2)
        with self.assertRaises(ValueError):
            i2 = _Instrument(n2,n1)

    def test_init_stringed_instrument(self):
        r = 7
        t = []
        for x in range(r):
            t.append(Note('e'+str(x)))
        i = _StringedInstrument(r, t, [1]*r)

        self.assertTrue(i.tuning == t)
        self.assertTrue(i.strings == r)
        self.assertTrue(i.semitones == [1]*r)
        self.assertTrue(i.lowest_note == Note('e0'))
        self.assertTrue(i.highest_note == Note('e6'))

if __name__ == '__main__':
    unittest.main()
