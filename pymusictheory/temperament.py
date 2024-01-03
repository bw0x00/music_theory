#!/usr/bin/env python3

from fractions import Fraction
import re


# definition of temperaments
class TwelveTET():
    _len = 12
    _precision = 2
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

    def get_note_frequency(self,root,distance,precision=None):
        """ Returns the frequency of note with 'distance' to 'root' frequency
        """
        if not precision:
            precision = self._precision
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


class CoreChromaticScale:
    _number_octaves = 9

    def __init__(self, note=('a4', 440), temperament=temperament['12TET']):
        """ Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided in addition. Default: A4=440Hz and 12TET"""

        if type(note) is not list and type(note) is not tuple:
            raise ValueError(f"Wrong anchor note type: {type(note)}")
        if temperament.get_note_frequency(note[1],temperament.length) != note[1]*2:
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
                    self._temperament.get_note_frequency(self._anchor,
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
        return self._temperament.get_note_frequency(self._anchor,
                                          distancetoc0-self._anchor_distance)

    def __iter__(self):
        s = []
        for l in self.get_octaves():
            s.extend(l)
        return s.__iter__()



if __name__ == "__main__":
    pass
