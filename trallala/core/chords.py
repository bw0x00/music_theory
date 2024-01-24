#!/usr/bin/env python3

""" Classes and methods used for Chords
"""

from functools import singledispatchmethod

from .scales import ChromaticScale, Scale
from . import notes
from . import intervals

# chord name to integeter notation mapping (semitone distance from root)
from ..config_chords import chord_integer


class Chord:
    """ Chord class

    Class usable to construct objects representing chords. Object supports the
    generation of notes.Note objects as well as the conversion of the voicing.

    """


    def __init__(self, chord, root, voicing=None,
                 chromaticscale=ChromaticScale()):
        """ Instaciates a Chord object

        Args:
            chord:
                Chord name from trallala.config_chords or list/ tuple of notes
                or pitchclasses
            root:
                pitchclass name of the root note of the chord.
            voicing:
                tuple of octave numbers. len(voicing) must be equal to the amount
                of notes in the resulting chord object.
            chromaticscale:
                Chromaticscale used for the calculation of the notes in this
                chord

        Raises:
            ValueError:
                Chord cannot be constructed from provided parameters

         """
        self._scale = chromaticscale
        self._root_index = self._scale.temperament.name_to_distance(root)
        self._root_name = root
        self._chord = self._dispatch_init(chord)
        if voicing:
            self._voicing = tuple(voicing)
        else:
            self._voicing = None

        if self._voicing and len(self._chord) != len(self._voicing):
            raise ValueError("len(voicing) != len(chord)")

    # prevent bug in singledispatchmethod https://bugs.python.org/issue41122
    @singledispatchmethod
    def _dispatch_init(self, chord):
        raise ValueError(f"Chord() not implemented for type(chord)={type(chord)}")

    @_dispatch_init.register
    def _1(self, chord: str):
        return chord_integer[self._scale.temperament.length][chord]

    @_dispatch_init.register(tuple)
    @_dispatch_init.register(list)
    def _2(self, chord):
        if isinstance(chord[0], intervals.Interval):
            c = self._chord_int_from_intervals(chord)
        else:
            c = chord
        for x in c:
            if not isinstance(x, int):
                raise ValueError("Chord definition must be from predefined"
                   + "chords or a list of integers "
                   +" (e.g., a major chord would be [0, 4, 7]")
        return tuple(sorted(c))

    def _chord_int_from_intervals(self, intervals):
        return tuple(x.distance for x in intervals)

    def get_chord_as_interval(self) -> tuple:
        """ Returns the chord as a  root note and intervals

        Returns:
            tuple(root, tuple(Interval1..n))
        """
        ret = []
        c = self.get_chord()
        for n in c[1:]:
            ret.append(n-c[0])

        return (c[0], tuple(ret))

    def get_chord(self) -> list:
        """ Returns the list with the notes of the chord.
        """
        chord = []
        if self._voicing is None:
            root = self._chord[0]+4*self._scale.temperament.length
            for e in self._chord:
                n = notes.Note(root + e, self._scale)
                chord.append(n)
        else:
            for e, note in enumerate(self._chord):
                n = note \
                    + self._scale.temperament.length * self._voicing[e]
                chord.append( notes.Note(n, self._scale)  )
        return chord

    def get_pitchclasses(self) -> list:
        """ Pitchlasses in this chord

        Returns:
            tuple(pitchlass1..n)
        """
        return tuple(notes.PitchClass(n) for n in self.get_chord())

    def get_frequencies(self) -> list:
        """ Returns the list of the frequencies of the chord.

        List can contain
        frequencies of multiple octaves. Optional: An list of octave numbers
        can be provided. List must be of equal length to the chord and
        transposes the corresponding chord note into the given octave.
        """
        chord = self.get_chord()

        freqs = []
        for e in chord:
            freqs.append(e.frequency)
        return freqs

    def __getitem__(self,key):
        return self.get_chord()[key]

    def __str__(self):
        return ", ".join(("/".join(self._scale.temperament.distance_to_name(x)) \
                for x in self._chord))

    @singledispatchmethod
    def __add__(self, a):
        return NotImplemented

    @__add__.register
    def _1(self, a: notes.Note):
        if not self._voicing:
            raise ValueError("Cannot add Note to Chord without set voicing")
        d = a.distance % self._scale.temperament.length
        o = int(a.distance / self._scale.temperament.length)
        c = list(self._chord)
        if d not in c:
            c.append(d)
            v = list(self._voicing)
            v.append(o)
        return Chord(c, root=self._root_name, voicing=v,
                     chromaticscale=self._scale)

    @__add__.register
    def _2(self, a: notes.PitchClass):
        new_chord_int = []
        new_chord_int.extend(self._chord)
        if a.numeric not in new_chord_int:
            new_chord_int.append(a.numeric)
            if self._voicing:
                v = list(self._voicing)
                v.append(v[0])
            else:
                v = None
        ret = Chord(new_chord_int, self._root_name, v, self._scale)
        return ret

    @__add__.register
    def _3(self, a: intervals.Interval):
        new_chord_int = list(self._chord)
        v = list(self._voicing[:])
        if a.distance not in new_chord_int:
            new_chord_int.append(a.distance)
            if v:
                if self._root_index + a.distance \
                    < self._scale.temperament.length:
                    v.append(v[0])
                else:
                    v.append(v[0] + 1)
        return Chord(new_chord_int, self._root_name, v ,self._scale)

    @singledispatchmethod
    def __eq__(self,a):
        if isinstance(a,  Chord):
            return self.get_chord() == a.get_chord()
        raise ValueError(f'__eq__ not defined for type {type(a)}')

    @__eq__.register(tuple)
    @__eq__.register(list)
    def _1(self, a ):
        if min(isinstance(x,int) for x in a):
            return self._chord == a
        if min(isinstance(x, intervals.Interval) for x in a):
            return self._chord == self._chord_int_from_intervals(a)
        if min(isinstance(x, str) for x in a):
            return self.get_chord() == a
        raise ValueError("Chord can only compared to lists/tuple containing"
                             + " int or Interval. Mixed content is not supported")

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
        for note in self._chord:
            if a == note - self._chord[0]:
                return True
        return False

    @__contains__.register
    def _4(self,a: float):
        if not self._voicing:
            raise ValueError("Cannot compare frequency to Chord without set voicing")
        return a in self.get_frequencies()

    @__contains__.register
    def _5(self,a: int):
        return float(a) in self

    def __iter__(self):
        return self.get_chord().__iter__()

    @property
    def chord_int(self):
        """ Chord as integer tuple
        """
        return self._chord[:]

    @property
    def voicing(self):
        """ Current voicing of this chord
        """
        if self._voicing:
            return self._voicing[:]
        return None

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
