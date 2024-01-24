#!/usr/bin/env python3

""" Core definitions of temperaments, steps per octace

    This packages supports TET12 by default. Additional temperaments can be
    added to the temperament dict and afterwards used to initialize a
    chromaticscale:

    temperament = {
        '12TET' : TwelveTET()
    }
"""

import re

from fractions import Fraction


# definition of temperaments
class TwelveTET():
    """ Definition of 12-TET

    Definition of the names and distances and frequency calculation used in
    a chromaticscale and therefore in all classes of this package.

    Properties:
        length:
            Length (amount of steps) in an octave

    """
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
        reverse_semitone_distance = {}
        for k, value in self._semitone_distance.items():
            j = value
            try:
                reverse_semitone_distance[j].append(k)
            except KeyError:
                reverse_semitone_distance[j] = [k]
        self._reverse_semitone_distance = reverse_semitone_distance

    def __len__(self):
        return self._len

    def get_note_frequency(self, root, distance, precision=None):
        """ Returns the frequency of note with 'distance' to 'root' frequency

        Args:
            root:
                root frequency used to calculate the target frequency
            distance:
                Semitone-step distance of target from root
            precision:
                Floating point precision of the return
        Returns:
            Frequency as float
        """
        if not precision:
            precision = self._precision
        return round(root * ((2**Fraction(1, self._len)) ** distance), precision)

    def distance_to_name(self, distance):
        """ Translates any note distance to the name of the pitch class (int)

        Args:
            distance:
                semitone distance to C. Must be int with a value in
                range(self.length)
        Returns:
            Name of pitchclass as str
        Raises:
            KeyError:
                Distance > self.length
        """
        return self._reverse_semitone_distance[distance]

    def name_to_distance(self, name):
        """Translates a name of a pitchclass into the semitone distance.

        Args:
            name:
                Name of pitchclass without added octave
        Returns:
            Numeric name of the pitchclass (name without added octave)
        Raises:
            ValueError:
                Unknown name

        """
        name = name.lower()
        if name in self._semitone_distance:
            return self._semitone_distance[name]
        raise ValueError(
                f'Bad note name "{name}". Note name of pitchclass required')

    @property
    def length(self):
        """ Length of temperament
        """
        return self._len


temperament = {}


def _init_temperament():
    """ Initializtion of temperament dict
    """
    # Equal Temeperament
    temperament['12TET'] = TwelveTET()


_init_temperament()


class _CoreChromaticScale:
    """ 'Raw' ChromaticScales used by Notes and PitchClasses

    This 'raw' Class is used to prevent circular dependencies of the classes
    in this package and does not support higher level data types.

    Please use trallala.core.scales.ChromaticSclae instead.

    !DO NOT USE THIS CLASS OUTSIDE OF TRALLALA!

    """
    _number_octaves = 9

    def __init__(self, note=('a4', 440), temperament=temperament['12TET']):
        """ Warning: Internal Class only. Please use ChromaticScale instead.

        Creates Chromatic Scale from given note (Scientific Pitch Notation)
        and a temperament distance list. For non-12 steps scales, a list of
        tone with the correpsonding half-tone distance must be be provided
        in addition. Default: A4=440Hz and 12TET"""

        if not isinstance(note, (list, tuple)):
            raise ValueError(f"Wrong anchor note type: {type(note)}")
        if temperament.get_note_frequency(note[1], temperament.length) != note[1]*2:
            raise ValueError('len(temperament) != one octave')

        self._temperament = temperament
        self._anchor = note[1]
        self._anchor_distance = self.spn_to_distance(note[0])

    def get_octaves(self):
        """ returns a full octave from An to An+1 (including). i.e., the list
        is len(temperament)+1 """
        octaves = {}
        for o in range(self._number_octaves):
            octaves[o] = self._calc_octave(o)
        return octaves

    def _calc_octave(self, octave_number):
        """ Calculates the octave number n from Cn to Cn+1 """
        ret = []
        for i in range(len(self._temperament)+1):
            ret.append(
                self._temperament.get_note_frequency(self._anchor,
                                                     self.temperament.length*octave_number \
                                                        -self._anchor_distance + i))
        return ret

    @property
    def temperament(self):
        """  Temperament used by this ChromaticScale
        """
        return self._temperament

    @property
    def anchor(self):
        """ Used Anchor not as (SPN, Frequency)
        """
        return (self.spn_from_distance(self._anchor_distance), self._anchor)

    def spn_to_distance(self, note: str):
        """ Calculates semitone distance of note in SPN to C0

        Arg:
            note:
                Note as SPN string

        Returns:
            Semitone distance to C0 as int
        """
        (note_name, octave) = self.split_spn(note)
        return int(octave) * self.temperament.length + self.temperament.name_to_distance(note_name)

    def spn_from_distance(self, distance: int):
        """ Semitone Distance to C= to SPN

        Args:
                distance:
                    Semitone distance to C0

        Returns:
            SPN name as str
        """
        l = len(self._temperament)
        note = self._temperament.distance_to_name(distance % l)
        octave = int((distance-distance % l) / l)
        return "/".join( [''.join((x,str(octave) )) for x in note]  )

    def split_spn(self, spn: str):
        """ Splits an SPN into note name and octave

        Args:
            spn:
                SPN name as str

        Returns:
            tuple(note name, octave)

        Raises:
            ValueError in case of invalid SPN

        """
        match = re.match(r"([abcdefg][b#]?)([0-9])", spn.lower(), re.I)
        if match:
            return match.groups()
        raise ValueError(f'Bad note name {spn}. Note name in SPN required')

    def frequencyof(self, distancetoc0):
        """ Frequency of a semitone distance to C0

        Args:
            distancetoc0:
                Semitone distance to C0 in int
        """
        return self._temperament.get_note_frequency(self._anchor,
                                                    distancetoc0-self._anchor_distance)

    def __iter__(self):
        s = []
        for l in self.get_octaves():
            s.extend(l)
        return s.__iter__()


if __name__ == "__main__":
    pass
