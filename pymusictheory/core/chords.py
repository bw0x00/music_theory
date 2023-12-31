#!/usr/bin/env python3

from functools import singledispatchmethod

from .scales import ChromaticScale, Scale
from . import notes
from . import intervals

# chord name to integeter notation mapping (semitone distance from root)
chord_integer = {
    12: {
        'powerchord'        : (0, 7),
        'powerchord2'       : (0, 7, 12),
        'major'             : (0, 4, 7),
        "major6"            : (0, 4, 7, 9),
        'major7'            : (0, 4, 7, 11),
		"major9"            : (0, 4, 7, 11, 14),
		"major11"           : (0, 4, 7, 11, 14, 17),
		"major13"           : (0, 4, 7, 11, 14, 17, 21),
		"sus2"              : (0, 2, 7),
		"sus4"              : (0, 5, 7),
		"dominant7"         : (0, 4, 7, 10),
		"dominant9"         : (0, 4, 7, 10, 14),
		"dominant11"        : (0, 4, 7, 10, 14, 17),
		"dominant13"        : (0, 4, 7, 10, 14, 17, 21),
        'minor'             : (0, 3, 7),
		"minor6"            : (0, 3, 7, 9),
		"minor7"            : (0, 3, 7, 10),
		"minorM7"           : (0, 3, 7, 11),
		"minor9"            : (0, 3, 7, 10, 14),
		"minor11"           : (0, 3, 7, 10, 14, 17),
		"diminished"        : (0, 3, 6),
		"diminished7"       : (0, 3, 6, 9),
		"half_diminished7"  : (0, 3, 6, 10),
		"augmented"         : (0, 4, 8),
		"augmented7"        : (0, 4, 8, 10),
		"dominant7sus4"     : (0, 5, 7, 10)
    }
}


class Chord:

    def __init__(self, chord, root, voicing=None,
                 chromaticscale=ChromaticScale()):
        """ Creates a Chord object for 'root' and 'chord' (integer list).
        'root' must be name of PitchClass (str) """
        self._scale = chromaticscale
        self._root_index = self._scale.temperament.name_to_distance(root)
        self._root_name = root
        self._chord = self._dispatch_init(chord, root, voicing, chromaticscale)
        if voicing:
            self._voicing = tuple(voicing)
        else:
            self._voicing = None

        if self._voicing and len(self._chord) != len(self._voicing):
            raise ValueError("len(voicing) != len(chord)")

    # prevent bug in singledispatchmethod https://bugs.python.org/issue41122
    @singledispatchmethod
    def _dispatch_init(self, chord, root, voicing, chromaticscale):
        raise ValueError(f"Chord() not implemented for type(chord)={type(chord)}")

    @_dispatch_init.register
    def _1(self, chord: str, root, voicing, chromaticscale):
        return chord_integer[chromaticscale.temperament.length][chord]

    @_dispatch_init.register(tuple)
    @_dispatch_init.register(list)
    def _2(self, chord , root, voicing, chromaticscale):
        if type(chord[0]) is intervals.Interval:
            c = self._chord_int_from_intervals(chord)
        else:
            c = chord
        for x in c:
           if type(x) is not int:
               raise ValueError("Chord definition must be from predefined"
                   + "chords or a list of integers "
                   +" (e.g., a major chord would be [0, 4, 7]")
        return tuple(sorted(c))

    def _chord_int_from_intervals(self, intervals):
        return tuple(x.distance for x in intervals)

    def get_chord(self) -> list:
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
        o = int(a.distance / self._scale.temperament.length)
        c = [x for x in self._chord]
        if d not in c:
            c.append(d)
            v = [x for x in self._voicing]
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
                v = [x for x in self._voicing]
                v.append(v[0])
            else:
                v = None
        ret = Chord(new_chord_int, self._root_name, v, self._scale)
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
        return Chord(new_chord_int, self._root_name, v ,self._scale)

    @singledispatchmethod
    def __eq__(self,a):
        if type(a) is Chord:
            return self.get_chord() == a.get_chord()
        else:
            raise ValueError(f'__eq__ not defined for type {type(a)}')

    @__eq__.register(tuple)
    @__eq__.register(list)
    def _1(self, a ):
        isint = True
        isinterval = True
        isstr = True
        for i in a:
            if type(i) is not int:
                isint = False
            if type(i) is not intervals.Interval:
                isinterval = False
            if type(i) is not str:
                isstr = False
        if isint:
            return self._chord == a
        elif isinterval:
            return self._chord == self._chord_int_from_intervals(a)
        elif isstr:
            return self.get_chord() == a
        else:
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
    def chord_int(self):
        return self._chord

    @property
    def voicing(self):
        if self._voicing:
            return self._voicing[:]
        else:
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
