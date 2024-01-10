import unittest

from fractions import Fraction
from pymusictheory.core.scales import Scale
from pymusictheory.core.notes import PitchClass, Note
from pymusictheory.core.chords import Chord
from pymusictheory.instruments.guitar import Guitar

class TestGuitar(unittest.TestCase):

    def test_init_guitar(self):
        n1 = Note('e2')
        n2 = Note('e6')
        g = Guitar()
        g2 = Guitar('e2',[Note(x) for x in ('e2','a2','d3','g3','b3','e4')])
        g3 = Guitar('e2',[0,5,5,5,4,5])

        for x in (g,g2,g3):
            self.longMessage = True
            self.assertTrue( x.lowest_note == n1,
                            f"{','.join([str(a) for a in x.tuning])}: "
                            + f"{str(x.lowest_note)} != {str(n1)}")
            self.assertTrue( x.highest_note == n2,
                            f"{','.join([str(a) for a in x.tuning])}: "
                            + f"{str(x.highest_note)} != {str(n2)}")


    def test_fretboard(self):
        g = Guitar()
        f = g.fretboard.all_notes
        self.assertTrue(len(f) == 6)
        self.assertTrue(min( (len(x) == 25 for x in f) ))


    def test_getindices(self):
        g = Guitar()
        f = g.fretboard
        i = f.get_indices(Note('e4'))
        i2 = f.get_indices(Chord(root='c',chord='major',voicing=(3,3,4)))
        i3 = f.get_indices(PitchClass('c'))
        i4 = f.get_indices(Scale('c'))


        for string, fret in i:
            self.assertTrue(f.all_notes[string][fret] == Note('e4'))


if __name__ == '__main__':
    unittest.main()
