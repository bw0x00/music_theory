#!/usr/bin/env python3

from functools import singledispatchmethod

from .scales import ChromaticScale
from . import notes
from . import intervals

# chord name to integeter notation mapping (semitone distance from root)
chord_integer = {
    12: {
        'powerchord'    : (0, 7),
        'powerchord2'   : (0, 7, 12),
        'major'         : (0, 4, 7),
        'major7'        : (0, 4, 7, 11),
        'minor'         : (0, 3, 7)
    }
}


class Chord:

    def __init__(self, root: str, chord, chromaticscale=ChromaticScale()):
        """ Creates a Chord object for 'root' and 'chord' (integer list).
        'root' must be name of PitchClass (str) """
        self._scale = chromaticscale
        self._root_index = self._scale.temperament.name_to_distance(root)
        self._root_name = root

        if type(chord) is str: # test if chord definition is in chord_inter
            self._chord = chord_integer[self._scale.temperament.length][chord]
        else: #chord definition must be integer list
            # test if chord is integer list
            for x in chord:
                if type(x) is not int:
                    raise ValueError("Chord definition must be from predefined"
                    + "chords or a list of integers "
                    +" (e.g., a major chord would be [0, 4, 7]")
            self._chord = sorted(chord)

    def get_chord(self, voicing: list = None) -> list:
        """ Returns the list with the notes of the chord. Optional: provide
        voicing as list of octaves per note in chord """
        chord = []
        if voicing is None:
            root = self._chord[0]+4*self._scale.temperament.length
            for e in self._chord:
                n = notes.Note(root + e, self._scale)
                chord.append(n)
        else:
            if len(voicing) != len(self._chord):
               raise ValueError("len(voicing) != len(chord)")
            else:
               for e in range(len(self._chord)):
                    n = self._chord[e] + 12 * voicing[e]
                    chord.append( notes.Note(n, self._scale)  )
        return chord

    def get_frequencies(self, voicing: list = None) -> list:
        """ Returns the list of the frequencies of the chord. List can contain
        frequencies of multiple octaves. Optional: An list of octave numbers
        can be provided. List must be of equal length to the chord and
        transposes the corresponding chord note into the given octave. """
        chord = self.get_chord(voicing)

        freqs = []
        for e in chord:
            freqs.append(e.frequency)
        return freqs

    def __str__(self):
        """ asdas """
        return ", ".join(("/".join(self._scale.temperament.distance_to_name(x)) for x in self._chord))

    @singledispatchmethod
    def __add__(self, a):
        raise ValueException(f"Unsupported type '{type(a)}'")

    # TODO: add for chord + note = chord
    @__add__.register
    def _1(self, a: notes.Note):
        pass

    @__add__.register
    def _2(self, a: notes.PitchClass):
        new_chord_int = []
        new_chord_int.extend(self._chord)
        new_chord_int.append(a.numeric)
        ret = Chord(self._root_name, new_chord_int, self._scale)
        return ret

    @singledispatchmethod
    def __eq__(self,a):
        if type(a) is Chord:
            return self.get_chord() == a.get_chord()
        else:
            raise ValueError(f'__eq__ not defined for type {type(a)}')

    @__eq__.register
    def _1(self, a: intervals.Interval):
        return self.get_chord()[::-1] == a

    @singledispatchmethod
    def __contains__(self,a):
        raise ValueError(f'__contains__ not defined for type {type(a)}')

    @__contains__.register
    def _1(self,a: notes.Note):
        pass

    @__contains__.register
    def _2(self,a: notes.PitchClass):
        pass

    @__contains__.register
    def _3(self,a: intervals.Interval):
        pass

    @__contains__.register
    def _4(self,a: float):
        pass

    @__contains__.register
    def _5(self,a: int):
        return self.__contains__(float(a)) 


if __name__ == '__main__':
    pass
