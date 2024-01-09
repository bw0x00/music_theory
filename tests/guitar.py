import unittest

from fractions import Fraction
from pymusictheory.core.scales import Scale
from pymusictheory.core.notes import PitchClass, Note
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


if __name__ == '__main__':
    unittest.main()
