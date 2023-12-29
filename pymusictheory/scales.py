#!/usr/bin/env python3

import re

from definitions import *


class ChromaticScale:
    _number_octaves = 9

    def __init__(self, note=('a4', 440), temperament=temperament['12TET'],
                 tone_distance=tone_distances['12']):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in addition. Default: A4=440Hz and 12TET"""
        if sum(temperament) != 1:
            raise ValueError('Fractions in "temperament" ' +
                             str(temperament) + '  don\'t sum up to 1')

        if len(set([x for x in tone_distance.values()])) != len(temperament):
            raise ValueError('len(temperament) != amount of tones in ' +
                             'tone_distance')

        self._temperament = temperament
        self._tone_distance = tone_distance
        self._freqA0 = self._calcA0(note, temperament)
        self._calc_octaves()

    def get_scale(self):
        return self._octaves

    def _calc_octaves(self):
        """ precalculates all octaves as self._octaves """
        self._octaves = dict()
        start = self._freqA0
        for octave in range(self._number_octaves+1):
            self._octaves[octave] = self._calc_octave(start)
            start = self._octaves[octave][-1]

    def _calc_octave(self, start):
        ret = list()
        ret.append(start)
        element = 0
        for i in range(len(self._temperament)):
            element = element + self._temperament[i]
            ret.append(start + start * element)
        return ret

    def _calcA0(self, note, temperament):
        """ Calculates A0 based on the given note (SPN, frequency) and temperament """
        match = re.match(r"([abcdefg][b#]?)([0-9])", note[0].lower(), re.I)
        if match:
            (note_name, octave) = match.groups()
        a = note[1] / (1 + sum(temperament[0:self._tone_distance[note_name]]))
        return a / 2**int(octave)


def test():
    a4 = ChromaticScale()
    c3_sci = ChromaticScale(note=('c3', 256))
    print(a4.get_scale())
    print(c3_sci.get_scale())


if __name__ == "__main__":
    test()
