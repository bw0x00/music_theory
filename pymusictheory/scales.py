#!/usr/bin/env python3

from fractions import Fraction

temperament = dict()

def init_temperament():
    # Equal Temeperament
    temperament['eq'] = [Fraction(1,12)]  * 12

init_temperament()

class ChromaticScale:
        _freq_root = None
        _temperament = None

        def __init__(self,temperament=temperament['eq']):
                self._freq_root = 440/16
                t = 0
                for e in temperament:
                    t = t + e
                if t != 1:
                    raise ValueError('Fractions in "temperament" don\'t sum up to 1')
                self._temperament = temperament

        def calc_octave(self,start=None):
            """ Starts from the frequency of the given A and builds the
            corresponding octave """
            if start == None:
                start = self._freq_root
            ret = list()
            ret.append(start)
            element = 0
            for i in range(len(self._temperament)):
                element = element + self._temperament[i]
                ret.append(start + start * element)
            return ret


def test():
    a = ChromaticScale()
    print(a.calc_octave())

if __name__ == "__main__":
    test()
