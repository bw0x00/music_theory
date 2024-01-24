#!/usr/bin/env python3

from functools import singledispatchmethod

from .temperament import _CoreChromaticScale
from . import notes
from ..config_intervals import reverse_interval_distance


class Interval:

    def __init__(self, interval, chromaticscale=_CoreChromaticScale()):
        """ Creates an Interval object based on a distance or the Interval
        name. Optional: Provide an alternative chromaticscale if 12TET is not
        used.
        """
        # TODO: use singledispatchmethod
        self._chromaticscale = chromaticscale
        self.reverse_interval_distance = reverse_interval_distance[chromaticscale.temperament.length]
        self._interval_distance = dict()
        for k in self.reverse_interval_distance:
            for n in self.reverse_interval_distance[k]:
                self._interval_distance[n] = k

        if type(interval) is int:
            self._distance = interval
            if interval < 0:
                raise ValueError('Interval cannot be created from negative'
                                 + ' distance')
        elif type(interval) is str:
           self._distance = self._interval_distance[interval]
           # ensure that name is always full name (e.g., major_fifth) 
           # and not short name. Exception: distance=6 --> 'tritone'
        else:
            raise ValueError("'interval' must be int or str, not"
                             + f"'{type(interval)}")
        if self._distance == 6 or self._distance == 18:
            self._name = self.reverse_interval_distance[self._distance][-1]
        else:
            self._name = self.reverse_interval_distance[self._distance][0]

    def __str__(self):
        return self._name

    @singledispatchmethod
    def __eq__(self, a):
        if type(a) == type(self):
            return a.name == self.name
        return NotImplemented

    @__eq__.register
    def _1(self,a: list):
        if len(a) == 2:
            for n in a:
                if type(n) is not notes.Note:
                    return NotImplemented
            d = a[0] - a[1]
            if d.distance == self._distance:
                return True

        else:
            return NotImplemented
        return False

    @__eq__.register
    def _2(self, a: tuple):
        return self == list(a)

    @__eq__.register
    def _3(self, a: int):
        return self._distance == a

    @singledispatchmethod
    def __lt__(self,a):
        if type(a) is Interval:
            return self.distance < a.distance
        else:
            return NotImplemented

    @__lt__.register
    def _1(self, a: int):
        return self.distance < a

    @singledispatchmethod
    def __radd__(self, a):
        return NotImplemented 

    @__radd__.register
    def __radd__(self, a: notes.Note):
        return a + self._distance

    @property
    def distance(self):
        return self._distance

    @property
    def longname(self):
        return self._name

    @property
    def name(self):
        return "/ ".join(self.short_names)

    @property
    def short_names(self):
        return self.reverse_interval_distance[self._distance][1:3]



# add note - note = interval to note class
@notes.Note.__sub__.register
def _n1(note1, note2: notes.Note):
    return Interval(note1.distance - note2.distance)

# add pitchclass + interval = pitchclass  to note pitchclass
@notes.PitchClass.__add__.register
def _n1(pc1, i: Interval):
    return notes.PitchClass(pc1.numeric + i.distance)



if __name__ == '__main__':
    pass
