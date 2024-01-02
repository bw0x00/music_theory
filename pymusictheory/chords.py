#!/usr/bin/env python3

from .scales import ChromaticScale
from .notes import Note, PitchClass

# chord name to integeter notation mapping (semitone distance from root)
chord_integer = {
        12 : {
            'major'             : (0,4,7),
            'major7'            : (0,4,7,11),
            'minor'             : (0,3,7)
            }
        }

class Chord:

    def __init__(self, root: str, chord: list, chromaticscale=ChromaticScale()):
        """ Creates a Chord object for 'root' and 'chord' (integer list).
        'root' must be name of PitchClass (str) """
        self._scale = chromaticscale
        self._root_index = self._scale.temperament.name_to_distance(root)
        self._chord = chord_integer[self._scale.temperament.length][chord]

    def get_chord(self, voicing: list =None) -> list:
        """ Returns the list with the notes of the chord. Optional: provide
        voicing as list of octaves per note in chord """
        if voicing is None:
            voicing = [4] * len(self._chord)
        else:
            voicing = [4] * voicing

        chord = []
        for e in range(len(self._chord)):
            n = Note(self._chord[e]) * (voicing[e] + 1)
            chord.append(n)
        return chord

    def get_frequencies(self, voicing: list =None) -> list:
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
        return ", ".join(( self._scale.temperament.distance_to_name(x) for x in self._chord ))

if __name__ == '__main__':
    pass
