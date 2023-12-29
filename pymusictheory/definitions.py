#!/usr/bin/env python3

from fractions import Fraction

temperament = dict()


def init_temperament():
    # Equal Temeperament
    temperament['12TET'] = [Fraction(1, 12)] * 12


init_temperament()

tone_distances = {
    '12': {
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

scales_steps = {
    'major'             : [2,2,1,2,2,2,1],
    'harmonic_major'    : [2,2,1,2,1,3,1],
    'melodic_major'     : [2,2,1,2,1,2,2],
    'minor'             : [2,1,2,2,1,2,2],
    'harmonic_minor'    : [2,1,2,2,1,3,1],
    'melodic_minor_up'  : [2,1,2,2,2,2,1],
    'melodic_minor_down': [2,2,1,2,2,1,2]
}

if __name__ == "__main__":
    pass
