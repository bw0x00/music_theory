#!/usr/bin/env python3

import re

from .definitions import *
from .converter import distance_to_note


class ChromaticScale:
    _number_octaves = 8

    def __init__(self, note=('a4', 440), temperament=temperament['12TET'],
                 tone_distance=tone_distances[12]):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in addition. Default: A4=440Hz and 12TET"""

        if len(set([x for x in tone_distance.values()])) != len(temperament):
            raise ValueError('temperament does not fit to the amount of tones in ' +
                             'tone_distance')

        self._temperament = temperament
        self._tone_distance = tone_distance
        self._freqA0 = self._calcA0(note, temperament)
        self._calc_octaves()

    def get_octaves(self):
        """ returns a full octave from An to An+1 (including). i.e., the list
        is len(temperament)+1 """
        return self._octaves

    def _calc_octaves(self):
        """ precalculates all octaves as self._octaves """
        self._octaves = dict()
        start = self._freqA0
        for octave in range(self._number_octaves+1):
            self._octaves[octave] = self._calc_octave(octave)
            start = self._octaves[octave][-1]

    def _calc_octave(self, octave_number):
        ret = list()
        for i in range(len(self._temperament)+1):
            ret.append(
                self._temperament.get_note(self._freqA0*2**octave_number, i))
        return ret

    def _calcA0(self, note, temperament):
        """ Calculates A0 based on the given note (SPN, frequency) and temperament """
        match = re.match(r"([abcdefg][b#]?)([0-9])", note[0].lower(), re.I)
        if match:
            (note_name, octave) = match.groups()
        a = self._temperament.get_note(note[1],
                                       (-1)*( 12*int(octave) + self._tone_distance[note_name]),
                                       precision=4)
        return a


class Scale(ChromaticScale):

    def __init__(self, root='c', scale='major',
                 _scales_steps=scales_steps[12],
                 note=('a4', 440), temperament=temperament['12TET'],
                 tone_distance=tone_distances[12]):
        """ Creates a scale of type 'scale' for 'root'  """
        if sum(_scales_steps[scale]) != len(temperament):
            raise ValueError('sum(scalesteps) != len(temperament)')

        try:
            tone_distance[root]
        except KeyError:
            raise ValueError('Undefined root note')

        self._scale_steps = _scales_steps[scale]
        self._root = root

        super().__init__(note, temperament, tone_distance)
        self._indices = self._calc_filter()

    def get_scale(self) -> list:
        """ Returns the notes of the scale as an list """
        reverse_tone_distance = distance_to_note(self._tone_distance)
        scale = []
        for k in self._indices:
            try:
                scale.append(reverse_tone_distance[k])
            except KeyError:
                pass
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
        """ Returns the frequencies of all hearable octaves """
        octaves = dict()
        for octave in self._octaves:
            octaves[octave] = []
            for k in sorted(self._indices):
                octaves[octave].append(self._octaves[octave][k])
        return octaves


if __name__ == "__main__":
    pass
