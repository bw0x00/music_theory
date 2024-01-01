#!/usr/bin/env python3

from functools import singledispatchmethod

from .definitions import *
from .scales import ChromaticScale
from .converter import distance_to_note


class Note:

    @singledispatchmethod
    def __init__(self, note, chromaticscale=ChromaticScale()):
        """ Creates a Note Object from another Note object, SPN, distance to C0 (int) or a frequency
        (float)."""
        if type(note) == type(self):
            self._shared_init(note.distance, chromaticscale)
        else:
            raise ValueError("Note must be initilized with SPN, int distance to C0" +
                         " or a frequence")


    @__init__.register
    def _1(self, note: int, chromaticscale=ChromaticScale()):
        self._shared_init(distancetoc0=note,chromaticscale=chromaticscale)

    @__init__.register
    def _2(self, note: float, chromaticscale=ChromaticScale()):
        success = False
        octaves = chromaticscale.get_octaves()
        for octave in octaves:
            for n in octaves[octave]:
                if n == note:
                    success = True
                    self._shared_init(len(octaves)-1*octave+n, chromaticscale)

        if not success:
            raise ValueError("Frequency does not match any note in used" +
                                " chromatic scale")

    @__init__.register
    def _3(self, note: str, chromaticscale=ChromaticScale()):
        self._shared_init(chromaticscale.SPN_to_distance(note),chromaticscale)

    def _shared_init(self, distancetoc0, chromaticscale):
        self._name = chromaticscale.SPN_from_distance(distancetoc0)
        self._distance = distancetoc0
        self._chromaticscale = chromaticscale

    @singledispatchmethod
    def __eq__(self,a):
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
        # TODO: improve performance
        octaves = self._chromaticscale.get_octaves()
        for octave in octaves:
            for note in octaves[octave]:
                if note == a:
                    return True
        return false

    @__eq__.register
    def _3(self, a: str):
        return a.lower() == self.name

    @singledispatchmethod
    def __gt__(self,a):
        if type(a) == type(self):
            return a.distance < self.distance
        else:
            raise TypeError("unsupported operand types(s) for __eq__")

    @__gt__.register
    def _1(self, a: int):
        return a <  self.distance

    @__gt__.register
    def _2(self, a: float):
        return a < self.frequency

    @__gt__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) < self.distance

    @singledispatchmethod
    def __lt__(self,a):
        if type(a) == type(self):
            return a.distance > self.distance
        else:
            raise TypeError("unsupported operand types(s) for __eq__")

    @__lt__.register
    def _1(self, a: int):
        return a >  self.distance

    @__lt__.register
    def _2(self, a: float):
        return a > self.frequency

    @__lt__.register
    def _3(self, a: str):
        return self._chromaticscale.SPN_to_distance(a) > self.distance



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

    def __init__(self, note, chromaticscale=ChromaticScale()):
        """ Creates the PitchClass containing 'note' """
        pass

if __name__ == '__main__':
    pass
