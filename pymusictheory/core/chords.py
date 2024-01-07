#!/usr/bin/env python3

from functools import singledispatchmethod

from .scales import ChromaticScale, Scale
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

    def __init__(self, root: str, chord, voicing=None,
                 chromaticscale=ChromaticScale()):
        """ Creates a Chord object for 'root' and 'chord' (integer list).
        'root' must be name of PitchClass (str) """
        self._scale = chromaticscale
        self._root_index = self._scale.temperament.name_to_distance(root)
        self._root_name = root
        if voicing:
            self._voicing = tuple(voicing)
        else:
            self._voicing = None

        if type(chord) is str: # test if chord definition is in chord_inter
            self._chord = chord_integer[self._scale.temperament.length][chord]
        else: #chord definition must be integer list
            # test if chord is integer list
            for x in chord:
                if type(x) is not int:
                    raise ValueError("Chord definition must be from predefined"
                    + "chords or a list of integers "
                    +" (e.g., a major chord would be [0, 4, 7]")
            self._chord = tuple(sorted(chord))
        if self._voicing and len(self._chord) != len(self._voicing):
            raise ValueError("len(voicing) != len(chord)")

    def get_chord(self, voicing: list = None) -> list:
        """ Returns the list with the notes of the chord. Optional: provide
        voicing as list of octaves per note in chord """
        chord = []
        if self._voicing is None:
            root = self._chord[0]+4*self._scale.temperament.length
            for e in self._chord:
                n = notes.Note(root + e, self._scale)
                chord.append(n)
        else:
            for e in range(len(self._chord)):
                n = self._chord[e] \
                    + self._scale.temperament.length * self._voicing[e]
                chord.append( notes.Note(n, self._scale)  )
        return chord

    def get_frequencies(self) -> list:
        """ Returns the list of the frequencies of the chord. List can contain
        frequencies of multiple octaves. Optional: An list of octave numbers
        can be provided. List must be of equal length to the chord and
        transposes the corresponding chord note into the given octave. """
        chord = self.get_chord()

        freqs = []
        for e in chord:
            freqs.append(e.frequency)
        return freqs

    def __str__(self):
        """ asdas """
        return ", ".join(("/".join(self._scale.temperament.distance_to_name(x)) for x in self._chord))

    @singledispatchmethod
    def __add__(self, a):
        return NotImplemented

    @__add__.register
    def _1(self, a: notes.Note):
        if not self._voicing:
            raise ValueError("Cannot add Note to Chord without set voicing")
        d = a.distance % self._scale.temperament.length
        o = round(a.distance / self._scale.temperament.length)
        c = [x for x in self._chord]
        if d not in c:
            c.append(d)
            v = [x for x in self._voicing]
            v.append(o)
        return Chord(root=self._root_name, chord=c, voicing=v,
                     chromaticscale=self._scale)

    @__add__.register
    def _2(self, a: notes.PitchClass):
        new_chord_int = []
        new_chord_int.extend(self._chord)
        if a.numeric not in new_chord_int:
            new_chord_int.append(a.numeric)
            if self._voicing:
                v = [x for x in self._voicing]
                v.append(v[0])
            else:
                v = None
        ret = Chord(self._root_name, new_chord_int, v,self._scale)
        return ret

    @__add__.register
    def _3(self, a: intervals.Interval):
        new_chord_int = [x for x in self._chord]
        v = list(self._voicing[:])
        if a.distance not in new_chord_int:
            new_chord_int.append(a.distance)
            if v:
                if self._root_index + a.distance \
                    < self._scale.temperament.length:
                    v.append(v[0])
                else:
                    v.append(v[0] + 1)
        return Chord(self._root_name, new_chord_int, v ,self._scale)

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
        """ Checks if a note, pitchclass or interval is in the chord:
        - Note is checked based on defined voicing of chord and exact note value
        - pitchclass is checked based on it's numeric independ from chord
          voicing
        - interval is checked based on the distance of all notes in the chord
          to the root note
        """
        if self._voicing is None:
            raise ValueError("Cannot compare note to Chord without set voicing")
        return a.name in self.get_chord()

    @__contains__.register
    def _2(self,a: notes.PitchClass):
        return a.numeric in self._chord

    @__contains__.register
    def _3(self,a: intervals.Interval):
        for i in range(len(self._chord)):
            if self._chord[i] - self._chord[0]:
                return True
        return False

    @__contains__.register
    def _4(self,a: float):
        if not self._voicing:
            raise ValueError("Cannot compare frequency to Chord without set voicing")
        return a in self.get_frequencies()

    @__contains__.register
    def _5(self,a: int):
        return self.__contains__(float(a))

    @property
    def voicing(self):
        return self._voicing[:]

    @voicing.setter
    def voicing(self, voicing):
        if len(voicing) == len(self._chord):
            self._voicing = tuple(voicing)
        else:
            raise ValueError("len(voicing) not equal len(chord)")

@Scale.__contains__.register
def _s1(scale, a: Chord):
    for chord_note in a.get_chord():
        if chord_note not in scale:
            return False
    return True

if __name__ == '__main__':
    pass
