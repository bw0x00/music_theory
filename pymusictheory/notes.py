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
            pass
        else:
            raise ValueError("Note must be initilized with SPN, int distance to C0" +
                         " or a frequence")


    @__init__.register
    def _(self, note: int, chromaticscale=ChromaticScale()):
        self._shared_init(name=chromaticscale.SPN_from_distance(note),
                          distancetoc0=note,chromaticscale=chromaticscale)

    @__init__.register
    def _(self, note: float):
        pass

    @__init__.register
    def _(self, note: str, chromaticscale=ChromaticScale()):
        pass

    def _shared_init(self, name, distancetoc0, chromaticscale):
        self._name = name
        self._distancetoc0 = distancetoc0
        self._chromaticscale = chromaticscale

    @singledispatchmethod
    def __eq__(self,a,b):
        if type(note) == type(self):
            pass
        else:
            raise TypeError("unsupported operand types(s) for __eq__")

    @__eq__.register
    def _(self, note: int):
        pass

    @__eq__.register
    def _(self, note: float):
        pass

    @__eq__.register
    def _(self, note: str):
        pass

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def distancetoc0(self):
        return self._distancetoc0

    @property
    def frequency(self):
        return self._chromaticscale.frequencyof(self._distancetoc0)


class PitchClass:

    def __init__(self, note, chromaticscale=ChromaticScale()):
        """ Creates the PitchClass containing 'note' """
        pass
    

if __name__ == '__main__':
    pass
