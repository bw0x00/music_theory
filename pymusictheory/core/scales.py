#!/usr/bin/env python3

import re
from functools import singledispatchmethod

from .temperament import _CoreChromaticScale
from .temperament import *
from . import notes
from . import intervals

# scale name to semitone distance from root
scales_steps = {
    12: {
        'major'                     : (2, 2, 1, 2, 2, 2, 1),
        'ionian'                    : (2, 2, 1, 2, 2, 2, 1),
        'dorian'                    : (2, 1, 2, 2, 2, 1, 2),
        'phrygian'                  : (1, 2, 2, 2, 1, 2, 2),
        'lyldian'                   : (2, 2, 2, 1, 2, 2, 1),
        'mixolydian'                : (2, 2, 1, 2, 2, 1, 2),
        'aeolian'                   : (2, 1, 2, 2, 1, 2, 2),
        'locrian'                   : (1, 2, 2, 1, 2, 2, 2),
        'harmonic_major'            : (2, 2, 1, 2, 1, 3, 1),
        'melodic_major'             : (2, 2, 1, 2, 1, 2, 2),
        'minor'                     : (2, 1, 2, 2, 1, 2, 2),
        'natural_minor'             : (2, 1, 2, 2, 1, 2, 2),
        'harmonic_minor'            : (2, 1, 2, 2, 1, 3, 1),
        'ascending_melodic_minor'   : (2, 1, 2, 2, 2, 2, 1),
        'descending_melodic_minor'  : (2, 2, 1, 2, 2, 1, 2),
        'minor_pentatonic'          : (3,    2, 2, 3   , 2),
        'major_pentatonic'          : (2, 2, 3,    2, 3   ),
        'japanese_pentatonic'       : (2, 3   , 2, 2, 3   ),
        'major_blues'               : (2, 1, 1, 3, 2, 3),
        'minor_blues_b5'            : (3, 2, 1, 1, 3, 2),
        'minor_blues_M3'            : (3, 1, 2, 1, 3, 2),
        'minor_blues_M7'            : (3, 2, 2, 3, 1, 1)
    }
}

#check integrity of scale_steps:
for t in scales_steps:
    for s in scales_steps[t]:
        if sum(scales_steps[t][s]) != t:
            raise ValueError(f"Sum of steps in {s}: {scales_steps[t][s]} != {t}")

# Indirection required to allow scales to work with Note objects
class ChromaticScale(_CoreChromaticScale):
    _number_octaves = 9

    def __init__(self, anchor=('a4', 440), temperament=temperament['12TET']):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in
        addition. Default: A4=440Hz and 12TET
        """

        super().__init__(anchor, temperament)

    def get_octaves(self):
        """ returns a full octave from An to An+1 (including). i.e., the list
        is len(temperament)+1 """
        octaves = dict()
        for o in range(self._number_octaves):
            octaves[o] = self._calc_octave(o)
        return octaves

    def _calc_octave(self, octave_number):
        """ Calculates the octave number n from Cn to Cn+1 and returns it as a
        list of Note objects"""
        ret = list()
        for i in range(len(self._temperament)+1):
            anchor = (self.SPN_from_distance(
                self._anchor_distance), self._anchor)
            ret.append(notes.Note(i+self.temperament.length*octave_number,
                                  chromaticscale=_CoreChromaticScale(anchor,
                                                                     temperament=self.temperament)))
        return ret

    def __iter__(self):
        """ overwrites __iter__ to enable Note object """
        s = []
        for l in self.get_octaves():
            s.extend(l)
        return s.__iter__()


class Scale(ChromaticScale):

    def __init__(self, root='c', scale='major',
                 anchor=('a4', 440), temperament=temperament['12TET']):
        """ Creates a scale of type 'scale' for 'root'
        """

        super().__init__(anchor, temperament)

        # test if root is valid (i.e Pitchclass or Pitchclass name) ->
        # name_to_distance raises exception if invalid
        if type(root) is not notes.PitchClass:
            self._root  = notes.PitchClass(str(root), super())
        else:
            self._root = root

        if scale not in scales_steps[self.temperament.length]:
            raise ValueError(f"Unknown scale {scale}")
        elif sum(scales_steps[self.temperament.length][scale]) != self.temperament.length:
            raise ValueError(f"Sum of steps in {scale} != {t}")
        else:
            self._scalename = scale

        self._indices = self._calc_filter()

    def get_scale(self) -> list:
        """ Returns the notes of the scale as an list containing the pitchclass
        names
        """
        scale = []
        for k in self._indices:
            scale.append(notes.PitchClass(k))
        return scale

    def get_scale_frequencies(self, start_octave=4) -> list:
        """ Returns one octave of the starting with the root key in octave
        'start_octave'
        """
        root_to_anchor = self._root.numeric \
                        + self.temperament.length * start_octave \
                        - self._anchor_distance
        scale = []
        i = 0
        for k in scales_steps[self.temperament.length][self._scalename]:
            try:
                scale.append(self.temperament.get_note_frequency(self._anchor,
                                                                 root_to_anchor + i))
                i = i + k
            except KeyError:
                pass
        return scale

    def _calc_filter(self):
        indices = []
#        i = self.temperament.name_to_distance(self._root)
        i = self._root.numeric
        for step in scales_steps[self.temperament.length][self._scalename]:
            indices.append(i)
            i = (i + step) % self.temperament.length
        return indices

    def get_octaves(self):
        """ Returns the frequencies of the scale in all octaves in the used chromatic scale
        """
        octaves = dict()
        for octave in super().get_octaves():
            octaves[octave] = []
            for k in sorted(self._indices):
                octaves[octave].append(super().get_octaves()[octave][k])
        return octaves

    def __str__(self):
        return ", ".join((str(x) for x in self.get_scale()))

    def __iter__(self):
        s = []
        for l in self.get_scale():
            s.extend(l)
        return s.__iter__()

    @singledispatchmethod
    def __contains__(self,a):
        return NotImplemented

    @__contains__.register
    def _1(self, a: notes.PitchClass):
        return a.numeric in self._indices

    @__contains__.register
    def _2(self, a:intervals.Interval):
        return notes.Note(self._root.numeric + a) in self

    @__contains__.register
    def _3(self, a: notes.Note):
        structured_scale = self.get_octaves()
        octave = int(self.SPN_to_distance(a.name) \
                        / self.temperament.length)

        return str(a) in  structured_scale[octave]

    # !!! __contains__ for Chord added by .chords !!!!

if __name__ == "__main__":
    pass
