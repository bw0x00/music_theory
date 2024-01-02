#!/usr/bin/env python3

from fractions import Fraction
import re


# definition of temperaments
class TwelveTET():
    _len = 12
    _semitone_distance = {
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

    def __init__(self):
        reverse_semitone_distance = dict()
        for k in self._semitone_distance:
            j = self._semitone_distance[k]
            try:
                reverse_semitone_distance[j].append(k)
            except KeyError:
                reverse_semitone_distance[j] = [k]
        self._reverse_semitone_distance = reverse_semitone_distance

    def __len__(self):
        return self._len

    def get_note(self,root,distance,precision=2):
        return round(root * ( (2**Fraction(1,self._len)) **distance),precision)

    def distance_to_name(self, distance):
        """ Translates any note distance to the number of the pitch class (int) """
        return self._reverse_semitone_distance[distance]

    def name_to_distance(self,name):
        if name in self._semitone_distance:
            return self._semitone_distance[name]
        else:
            raise ValueError(f'Bad note name "{name}". Note name of pitchclass required')

    @property
    def length(self):
        return self._len

temperament = dict()

def init_temperament():
    # Equal Temeperament
    temperament['12TET'] = TwelveTET()

init_temperament()

if __name__ == "__main__":
    pass
