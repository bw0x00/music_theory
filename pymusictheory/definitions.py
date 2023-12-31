#!/usr/bin/env python3

from fractions import Fraction

# definition of temperaments
class TwelveTET():
    _len = 12

    def __init__(self):
        pass

    def __len__(self):
        return self._len

    def get_note(self,root,distance,precision=2):
        return round(root * ( (2**Fraction(1,12)) **distance),precision)

temperament = dict()

def init_temperament():
    # Equal Temeperament
    temperament['12TET'] = TwelveTET()

init_temperament()

# note to semi tone distance to A
semitone_distances = {
    12: {
        'a' : 9,
        'a#': 10,
        'bb': 10,
        'b' : 11,
        'c' : 0,
        'c#': 1,
        'db': 1,
        'd' : 2,
        'd#': 3,
        'eb': 3,
        'e' : 4,
        'f' : 5,
        'f#': 6,
        'gb': 6,
        'g' : 7,
        'g#': 8,
        'ab': 8
    }
}

# scale name to semitone distance from root
scales_steps = {
    12 : {
        'major'                         : (2,2,1,2,2,2,1),
        'harmonic_major'                : (2,2,1,2,1,3,1),
        'melodic_major'                 : (2,2,1,2,1,2,2),
        'minor'                         : (2,1,2,2,1,2,2),
        'harmonic_minor'                : (2,1,2,2,1,3,1),
        'ascending_melodic_minor'       : (2,1,2,2,2,2,1),
        'descending_melodic_minor'      : (2,2,1,2,2,1,2)
    }
}

# chord name to integeter notation mapping (semitone distance from root)
chord_integer = {
    12 : {
        'major'             : (0,4,7),
        'major7'            : (0,4,7,11),
        'minor'             : (0,3,7)
    }
}

if __name__ == "__main__":
    pass
