#!/usr/bin/env python3

"""Note and PitchClass Class definitions

PitchClasses and Notes are fundamentel datatypes for this
music theory package and are used and supported by all other
classes like scales, chords or instruments.
"""

from functools import singledispatchmethod
import re

from .temperament import _CoreChromaticScale

class Note:
    """Object representing a Note

    The Note object supports the initilization from different datatypes and
    supports several mathematical operations on top of if.

    Furthermore the Note Class is used as a fundamental class  and is supported
    by all other classes in trallala.

    Porperties:
        name:
            SPN name of the Note
        distance:
            Semitone distance to C0
        frequency:
            Frequency in Hz of the note
    """
    @singledispatchmethod
    def __init__(self, note, chromaticscale=_CoreChromaticScale()):
        """ Initializes a Note Object

        Creates a Note Object from another Note object, SPN, distance to C0 (int) or a frequency
        (float).

        Args:
            note:
                Note, SPN (str), distance to C0 (int) or frequency (float)
            chromaticscale:
                ChromaticScale Object. Default: TET12
        Raises:
            ValueError:
                Frequency, SPN, distance does not usable to create note from
        """
        if type(note) == type(self):
            self._shared_init(note.distance, chromaticscale)
        else:
            raise ValueError("Note must be initilized with SPN, int distance to C0"
                             + " or a frequence")

        if type(chromaticscale) is not _CoreChromaticScale:
            chromaticscale = _CoreChromaticScale(chromaticscale.anchor,
                                                 chromaticscale.temperament)

    @__init__.register
    def _1(self, note: int, chromaticscale=_CoreChromaticScale()):
        if type(chromaticscale) is not _CoreChromaticScale:
            chromaticscale = _CoreChromaticScale(chromaticscale.anchor,
                                                 chromaticscale.temperament)
        self._shared_init(distancetoc0=note, chromaticscale=chromaticscale)

    @__init__.register
    def _2(self, note: float, chromaticscale=_CoreChromaticScale()):
        if type(chromaticscale) is not _CoreChromaticScale:
            chromaticscale = _CoreChromaticScale(chromaticscale.anchor,
                                                 chromaticscale.temperament)
        success = False
        octaves = chromaticscale.get_octaves()
        for octave in octaves:
            for n in octaves[octave]:
                if n == note:
                    success = True
                    distancec0 = octaves[octave].index(n) \
                                    + chromaticscale.temperament.length \
                                    * (octave)
                    self._shared_init(distancec0, chromaticscale)

        if not success:
            raise ValueError("Frequency does not match any note in used"
                             + " chromatic scale")

    @__init__.register
    def _3(self, note: str, chromaticscale=_CoreChromaticScale()):
        if type(chromaticscale) is not _CoreChromaticScale:
            chromaticscale = _CoreChromaticScale(chromaticscale.anchor,
                                                 chromaticscale.temperament)
        self._shared_init(chromaticscale.SPN_to_distance(note), chromaticscale)

    def _shared_init(self, distancetoc0, chromaticscale):
        self._name = chromaticscale.SPN_from_distance(distancetoc0)
        self._distance = distancetoc0
        self._chromaticscale = chromaticscale

    @singledispatchmethod
    def __eq__(self, a):
        """ Equal tests based on SPN, frequency or distance
        """
        if type(a) == type(self):
            return a.name == self.name
        else:
            return NotImplemented 

    @__eq__.register
    def _1(self, a: int):
        if a == self.distance:
            return True
        else:
            return self == float(a)

    @__eq__.register
    def _2(self, a: float):
        return self.frequency == a

    @__eq__.register
    def _3(self, a: str):
        return a.lower() == self.name

    @singledispatchmethod
    def __ge__(self, a):
        if type(a) == type(self):
            return a.distance <= self.distance
        else:
            return NotImplemented

    @__ge__.register
    def _1(self, a: int):
        return a <= self.distance

    @__ge__.register
    def _2(self, a: float):
        return a <= self.frequency

    @__ge__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) <= self.distance

    @singledispatchmethod
    def __le__(self, a):
        if type(a) == type(self):
            return a.distance >= self.distance
        else:
            return NotImplemented

    @__le__.register
    def _1(self, a: int):
        return a >= self.distance

    @__le__.register
    def _2(self, a: float):
        return a >= self.frequency

    @__le__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) >= self.distance

    @singledispatchmethod
    def __gt__(self, a):
        if type(a) == type(self):
            return a.distance < self.distance
        else:
            return NotImplemented

    @__gt__.register
    def _1(self, a: int):
        return a < self.distance

    @__gt__.register
    def _2(self, a: float):
        return a < self.frequency

    @__gt__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) < self.distance

    @singledispatchmethod
    def __lt__(self, a):
        if type(a) == type(self):
            return a.distance > self.distance
        else:
            return NotImplemented

    @__lt__.register
    def _1(self, a: int):
        return a > self.distance

    @__lt__.register
    def _2(self, a: float):
        return a > self.frequency

    @__lt__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) > self.distance

    @singledispatchmethod
    def __sub__(self, a):
        return NotImplemented

    @__sub__.register
    def _1(self, a: int):
        return Note(self.distance-a, self._chromaticscale)

    #!!! __sub__ for type(note) will be registered from .intervals !!!

    @singledispatchmethod
    def __add__(self, a):
        return NotImplemented

    @__add__.register
    def _1(self, a: int):
        return Note(self.distance+a, self._chromaticscale)

    def __mul__(self, a):
        """ Note can be multiplied with numbers > 0. Multiplication of a note
        is implemented as the addition of (a-1)*octave_length semitone steps.
        """
        if a >= 1:
            return Note(int(self.distance+(a-1)*self._chromaticscale.temperament.length),
                                self._chromaticscale)
        elif 0 < a < 1:
            return self/(1/a)
        else:
            raise TypeError(
                "Multiplication of 'Note' with numbers <= 0 not allowed")

    def __rtruediv__(self, a: int):
        """ not implemented; Throws TypeError if called """
        raise TypeError("Cannot divide by 'Note'")

    def __truediv__(self, a):
        """ Note can be divided by numbers > 0. Devision of a note is
        implemented as the substraction of (a-1)*octave_length semitone steps. """
        if a >= 1:
            return Note(int(self.distance-(a-1)*self._chromaticscale.temperament.length),
                                self._chromaticscale)
        elif 1 > a > 0:
            return self * (1/a)
        else:
            raise ValueError(
                "Division of 'Note' with numbers <= 0 not allowed")

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def distance(self):
        """ Distance to C0 """
        return self._distance

    @property
    def frequency(self):
        return self._chromaticscale.frequencyof(self._distance)


class PitchClass:
    """Object representing a ptichclass (e.g. all C notes in all octaves)

    Properties:
        numeric:
            Numeric representation (i.e., 0 to 11)
        name:
            Str name of the PichClass (e.g. C,D... without added octave)
    """

    def __init__(self, note, chromaticscale=_CoreChromaticScale()):
        """ initializes the PitchClass 

        Pitchclass can be initialized from a note, SPN,  distance to C0,
        PitchClass numeric (c=0,...) or frequency

        Args:
            note:
                Refernce value for the intialization. Can be any of Note, SPN,
                str name (e.g. 'a' without added octave), distance to C0 or frequency.
            chromaticscale:
                ChromaticScale used to for the definition. Default: TET12

        Raises:
        """
        try:
            n = Note(note)
        except ValueError:
            # if note name and not SPN is provided...
            n = Note("".join((note, '0')))

        self._chromaticscale = chromaticscale

        self._pc_numeric = n.distance % chromaticscale.temperament.length
        self._pc_name = chromaticscale.split_SPN(n.name)[0]
        pc = list()
        octaves = chromaticscale.get_octaves()
        for octave in octaves:
            pc.append(Note(self._pc_numeric)*(octave+1))
        self._pc = pc

    def __iter__(self):
        return self._pc.__iter__()

    def __str__(self):
        return str(", ".join((str(x) for x in self._pc)))

    def __getitem__(self, n):
        return self._pc[n]

    @singledispatchmethod
    def __eq__(self, a):
        if type(a) is PitchClass:
            return a.numeric == self.numeric
        else:
            return NotImplemented

    @__eq__.register
    def _1(self, a: str):
        return self._chromaticscale.temperament.name_to_distance(a)  == self._pc_numeric

    @__eq__.register
    def _2(self, a: list):
        for n in a:
            if self == n:
                return True
        return False

    @singledispatchmethod
    def __contains__(self,a):
        return NotImplemented

    @__contains__.register
    def _1(self, a: Note):
        return a.name in self._pc

    @__contains__.register(int)
    @__contains__.register(str)
    @__contains__.register(float)
    def _2(self, a):
        return Note(a, self._chromaticscale) in self

    @property
    def name(self):
        return self._pc_name

    @property
    def numeric(self):
        return self._pc_numeric


if __name__ == '__main__':
    pass
