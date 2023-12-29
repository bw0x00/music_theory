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

    def get_octaves(self):
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



class Scale(ChromaticScale):

    def __init__(self, root='c',scale='major', _scales_steps=scales_steps_12,
                 note=('a4',440), temperament=temperament['12TET'],
                 tone_distance=tone_distances['12']):
            if sum(_scales_steps[scale]) != len(temperament):
                raise ValueError('sum(scalesteps) != len(temperament)')

            try:
                tone_distance[root]
            except KeyError:
                raise ValueError('Undefined root note')

            self._scale_steps =  _scales_steps[scale]
            self._root = root

            super().__init__(note,temperament,tone_distance)
            self._indices =  self._calc_filter()


    def get_scale(self) -> list:
        reverse_tone_distance = dict()
        for k in self._tone_distance:
            if self._tone_distance[k] not in reverse_tone_distance:
                reverse_tone_distance[self._tone_distance[k]] = k
            else:
                reverse_tone_distance[self._tone_distance[k]] = \
                    (reverse_tone_distance[self._tone_distance[k]],
                                                 k)
        scale = []
        for k in self._indices:
            try:
                scale.append(reverse_tone_distance[k])
            except KeyError:
                pass
        print(self._indices)
        return scale


    def _calc_filter(self):
        indices = []
        i = self._tone_distance[self._root]
        for step in self._scale_steps:
            indices.append(i)
            i = (i + step) % len(self._temperament)
            if i == 0:
                indices.append(len(self._temperament))
        return indices


    def get_octaves(self):
        octaves = dict()
        for octave in self._octaves:
            octaves[octave] = []
            for k in sorted(self._indices):
                octaves[octave].append(self._octaves[octave][k])
        return octaves 


def test():
    print("Chromatic Scale")
    a4 = ChromaticScale()
    c3_sci = ChromaticScale(note=('c3', 256))
    print('A4: ' + str(a4.get_octaves()))
    print('C3_SCI: ' + str(c3_sci.get_octaves()))

    print("\nC Dur/ Major")
    cmaj = Scale()
    print(cmaj.get_scale())
    print("\nA Moll/ Minor")
    amin = Scale(root='a', scale='minor' )
    print(amin.get_scale())
    print("\nC# Moll/ Minor")
    cmin = Scale(root='c#', scale='minor' )
    print(cmin.get_scale())

if __name__ == "__main__":
    test()
