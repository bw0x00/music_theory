#!/usr/bin/env python3

from functools import singledispatchmethod
import re

from .temperament import _CoreChromaticScale

class Note:

    @singledispatchmethod
    def __init__(self, note, chromaticscale=_CoreChromaticScale()):
        """ Creates a Note Object from another Note object, SPN, distance to C0 (int) or a frequency
        (float).
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
                    self._shared_init(len(octaves)-1*octave+n, chromaticscale)

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
            raise TypeError("unsupported operand types(s) for __eq__")

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
    def __gt__(self, a):
        if type(a) == type(self):
            return a.distance < self.distance
        else:
            raise TypeError("unsupported operand types(s) for __eq__")

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
            raise TypeError("unsupported operand types(s) for __eq__")

    @__lt__.register
    def _1(self, a: int):
        return a > self.distance

    @__lt__.register
    def _2(self, a: float):
        return a > self.frequency

    @__lt__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) > self.distance

    def __add__(self, a):
        return Note(self.distance+a, self._chromaticscale)

    def __mul__(self, a):
        """ Note can be multiplied with numbers > 0. Multiplication of a note
        is implemented as the addition of (a-1)*octave_length semitone steps.
        """
        if a >= 1:
            return Note(round(self.distance+(a-1)*self._chromaticscale.temperament.length),
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
            return Note(round(self.distance-(a-1)*self._chromaticscale.temperament.length),
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

    def __init__(self, note, chromaticscale=_CoreChromaticScale()):
        """ Creates the PitchClass containing 'note'; 'note' can be any of SPN,
        distance to C0, PitchClass numeric (c=0,...) or frequency
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

    def __eq__(self, a):
        return self._pc_name == a

    @property
    def name(self):
        return self._pc_name

    @property
    def numeric(self):
        return self._pc_numeric


if __name__ == '__main__':
    pass
