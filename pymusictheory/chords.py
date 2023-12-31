#!/usr/bin/env python3

from .definitions import *
from .scales import ChromaticScale
from .converter import distance_to_note


class Chord:

    def __init__(self, root, chord, chromaticscale=ChromaticScale()):
        """ Creates a Chord object for root and chord. """
        self._scale = chromaticscale
        self._temperament_length = len(self._scale.get_octaves()[0])-1
        self._root_index = semitone_distances[self._temperament_length][root]
        self._chord = chord_integer[self._temperament_length][chord]

    def get_chord(self):
        """ Returns the list with the notes of the chord """
        td = semitone_distances[self._temperament_length]
        rtd = distance_to_note(td)
        chord = []
        for note in self._chord:
            chord.append(rtd[self._root_index + note])
        return chord

    def get_frequencies(self, voicing=None):
        """ Returns the list of the frequencies of the chord. List can contain
        frequencies of multiple octaves. Optional: An list of octave numbers
        can be provided. List must be of equal length to the chord and
        transposes the corresponding chord note into the given octave. """
        td = semitone_distances[self._temperament_length]
        chord = self.get_chord()
        if voicing is None:
            voicing = [3] * len(chord)
        freqs = []
        for e in range(len(chord)):
            freqs.append(self._scale.get_octaves()[
                         voicing[e]][td[chord[e][0]]])
        return freqs


if __name__ == '__main__':
    pass
