#!/usr/bin/env python3

from functools import singledispatchmethod

from .scales import ChromaticScale
# from .notes import Note, PitchClass
from . import notes

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
        if voicing is None:
            voicing = [4] * len(self._chord)
        else:
            voicing = [4] * voicing

        chord = []
        for e in range(len(self._chord)):
            n = notes.Note(self._chord[e]) * (voicing[e] + 1)
            chord.append(n)
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


if __name__ == '__main__':
    pass
