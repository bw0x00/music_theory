#!/usr/bin/env python3

import re

from .definitions import *
from .converter import distance_to_note


class ChromaticScale:
    _number_octaves = 9

    def __init__(self, note=('a4', 440), temperament=temperament['12TET'],
                 semitone_distance=semitone_distances[12]):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in addition. Default: A4=440Hz and 12TET"""

        if len(set([x for x in semitone_distance.values()])) != len(temperament):
            raise ValueError('temperament does not fit to the amount of tones in ' +
                             'semitone_distance')
        if temperament.get_note(note[1],len(temperament)) != note[1]*2:
            raise ValueError('len(temperament) != one octave')

        self._temperament = temperament
        self._semitone_distance = semitone_distance
        self._anchor=note[1]
        self._anchor_distance=self.calc_distance_to_C0(note[0])

    def get_octaves(self):
        """ returns a full octave from An to An+1 (including). i.e., the list
        is len(temperament)+1 """
        octaves = dict()
        for o in range(self._number_octaves):
            octaves[o] = self._calc_octave(o)
        return octaves

    def _calc_octave(self, octave_number):
        """ Calculates the octave number n from Cn to Cn+1 """
        ret = list()
        for i in range(len(self._temperament)+1):
            ret.append(
                self._temperament.get_note(self._anchor,
                                           12*octave_number-self._anchor_distance + i))
        return ret

    def calc_distance_to_C0(self,note):
        """ Calculates semitone distance of note in SPN to C0 """
        match = re.match(r"([abcdefg][b#]?)([0-9])", note.lower(), re.I)
        if match:
            (note_name, octave) = match.groups()
        else:
            raise ValueError('Bad note name. Note name in SPN required')
        return int(octave) * 12 + self._semitone_distance[note_name]


class Scale(ChromaticScale):

    def __init__(self, root='c', scale='major',
                 _scales_steps=scales_steps[12],
                 note=('a4', 440), temperament=temperament['12TET'],
                 semitone_distance=semitone_distances[12]):
        """ Creates a scale of type 'scale' for 'root'  """
        if sum(_scales_steps[scale]) != len(temperament):
            raise ValueError('sum(scalesteps) != len(temperament)')

        try:
            semitone_distance[root]
        except KeyError:
            raise ValueError('Undefined root note')

        self._scale_steps = _scales_steps[scale]
        self._root = root

        super().__init__(note, temperament, semitone_distance)
        self._indices = self._calc_filter()

    def get_scale(self) -> list:
        """ Returns the notes of the scale as an list """
        reverse_semitone_distance = distance_to_note(self._semitone_distance)
        scale = []
        for k in self._indices:
            try:
                scale.append(reverse_semitone_distance[k])
            except KeyError:
                pass
        return scale

    def _calc_filter(self):
        indices = []
        i = self._semitone_distance[self._root]
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
