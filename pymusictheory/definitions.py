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
tone_distances = {
    12: {
        'a' : 0,
        'a#': 1,
        'bb': 1,
        'b' : 2,
        'c' : 3,
        'c#': 4,
        'db': 4,
        'd' : 5,
        'd#': 6,
        'eb': 6,
        'e' : 7,
        'f' : 8,
        'f#': 9,
        'gb': 9,
        'g' : 10,
        'g#': 11,
        'ab': 11
    }
}

# scale name to semitone distance from root
scales_steps = {
    12 : {
        'major'             : (2,2,1,2,2,2,1),
        'harmonic_major'    : (2,2,1,2,1,3,1),
        'melodic_major'     : (2,2,1,2,1,2,2),
        'minor'             : (2,1,2,2,1,2,2),
        'harmonic_minor'    : (2,1,2,2,1,3,1),
        'melodic_minor_up'  : (2,1,2,2,2,2,1),
        'melodic_minor_down': (2,2,1,2,2,1,2)
    }
}

# chord name to integeter notation mapping (semitone distance from root)
chord_integer = {
    12 : {
        'major'             : (0,4,7),
        'minor'             : (0,3,7)
    }
}

if __name__ == "__main__":
    pass
