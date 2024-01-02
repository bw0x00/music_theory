#!/usr/bin/env python3

import re

from .definitions import *

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


class ChromaticScale:
    _number_octaves = 9

    def __init__(self, note=('a4', 440), temperament=temperament['12TET']):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in addition. Default: A4=440Hz and 12TET"""

        if temperament.get_note(note[1],len(temperament)) != note[1]*2:
            raise ValueError('len(temperament) != one octave')

        self._temperament = temperament
        self._anchor=note[1]
        self._anchor_distance=self.SPN_to_distance(note[0])

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

    @property
    def temperament(self):
        return self._temperament

    def SPN_to_distance(self,note):
        """ Calculates semitone distance of note in SPN to C0 """
        (note_name, octave) = self.split_SPN(note)
        return int(octave) * self.temperament.length + self.temperament.name_to_distance(note_name)

    def SPN_from_distance(self, distance: int):
        l = len(self._temperament)
        note = self._temperament.distance_to_name(distance % l)
        octave = int( ( distance-distance % l ) / l )
        return ''.join((note[0],str(octave)))

    def split_SPN(self, spn: str):
        match = re.match(r"([abcdefg][b#]?)([0-9])", spn.lower(), re.I)
        if match:
            return match.groups()
        else:
            raise ValueError(f'Bad note name {spn}. Note name in SPN required')


    def frequencyof(self, distancetoc0):
        return self._temperament.get_note(self._anchor,
                                          distancetoc0-self._anchor_distance)


class Scale(ChromaticScale):

    def __init__(self, root='c', scale='major',
                 anchor=('a4', 440), temperament=temperament['12TET']):
        """ Creates a scale of type 'scale' for 'root'  """


        super().__init__(anchor, temperament)

        # test if root is a valid note -> name_to_distance raises exception if invalid
        self.temperament.name_to_distance(root)

        if scale not in scales_steps[self.temperament.length]:
            raise ValueError(f"Unknown scale {scale}")
        else:
            self._scalename = scale

        self._root = root
        self._indices = self._calc_filter()

    def get_scale(self) -> list:
        """ Returns the notes of the scale as an list """
        scale = []
        for k in self._indices:
            scale.append( self.temperament.distance_to_name(k))
        return scale

    def get_scale_frequencies(self,start_octave=4) -> list:
        """ Returns one octave of the starting with the root key in octave
        'start_octave' """
        scale = []
        start_freq = self._calc_octave(start_octave)[self.temperament.name_to_distance(self._root)]
        i = 0
        for k in scales_steps[self.temperament.length][self._scalename]:
            try:
                scale.append(self.temperament.get_note(start_freq,i))
                i = i + k
            except KeyError:
                pass
        return scale

    def _calc_filter(self):
        indices = []
        i = self.temperament.name_to_distance(self._root)
        for step in scales_steps[self.temperament.length][self._scalename]:
            indices.append(i)
            i = (i + step) % self.temperament.length
        return indices

    def get_octaves(self):
        """ Returns the frequencies of the scale in all octaves in the used chromatic scale """
        octaves = dict()
        for octave in self._octaves:
            octaves[octave] = []
            for k in sorted(self._indices):
                octaves[octave].append(self._octaves[octave][k])
        return octaves

    def __str__(self):
        return ", ".join(( str(x) for x in self.get_scale()  ))

if __name__ == "__main__":
    pass
