#!/usr/bin/env python3

from functools import singledispatchmethod

from .temperament import _CoreChromaticScale
from . import notes

_reverse_interval_distance = {
        12: {
            0   : ('perfect_unison',        'P1',   'd2',   'root'          ),
            1   : ('minor_second',          'm2',   'A1',   'semitone'      ),
            2   : ('major_second',          'M2',   'd3',   'tone'          ),
            3   : ('minor_third',           'm3',   'A2'                    ),
            4   : ('major_third',           'M3',   'd4'                    ),
            5   : ('perfect_fourth',        'P4',   'A3'                    ),
            6   : ('tritone',               'd5',   'A4'                    ),
            7   : ('perfect_fifth',         'P5',   'd6'                    ),
            8   : ('minor_sixth',           'm6',   'A5'                    ),
            9   : ('major_sixth',           'M6',   'd7'                    ),
            10  : ('minor_seventh',         'm7',   'A6'                    ),
            11  : ('major_seventh',         'M7',   'd8'                    ),
            12  : ('perfect_octave',        'P8',   'A7',   'd9'            ),
            13  : ('minor_ninth',           'm9',   'A8'                    ),
            14  : ('major_ninth',           'M9',   'd10'                   ),
            15  : ('minor_tenth',           'm10',  'A9'                    ),
            16  : ('major_tenth',           'M10',  'd11'                   ),
            17  : ('perfect_eleventh',      'P11',  'A10'                   ),
            18  : (                         'd12',  'A11'                   ),
            19  : ('perfect_twelfth',       'P12',  'd13',  'tritave'       ),
            20  : ('minor_thirteenth',      'm13',  'A12'                   ),
            21  : ('major_thirteenth',      'M13',  'd14'                   ),
            22  : ('minor_fourteenth',      'm14',  'A13'                   ),
            23  : ('major_fourteenth',      'M14',  'd15'                   ),
            24  : ('perfect_fifteenth',     'P15',  'A14',  'double_octave' )
            }
        }


class Interval:

    def __init__(self, interval, chromaticscale=_CoreChromaticScale()):
        """ Creates an Interval object based on a distance or the Interval
        name. Optional: Provide an alternative chromaticscale if 12TET is not
        used.
        """
        self._chromaticscale = chromaticscale
        self._reverse_interval_distance = _reverse_interval_distance[chromaticscale.temperament.length]
        self._interval_distance = dict()
        for k in self._reverse_interval_distance:
            for n in self._reverse_interval_distance[k]:
                self._interval_distance[n] = k

        if type(interval) is int:
            self._distance = interval
            if interval < 0:
                raise ValueError('Interval cannot be created from negative'
                                 + ' distance')
            self._name = self._reverse_interval_distance[interval][0]
        elif type(interval) is str:
           self._distance = self._interval_distance[interval]
           # ensure that name is always full name (e.g., major_fifth) 
           # and not short name. Exception: distance=6 --> 'tritone'
           self._name = self._reverse_interval_distance[self._distance][0]
        else:
            raise ValueError("'interval' must be int or str, not"
                             + f"'{type(interval)}")

    def __str__(self):
        return self._name

    @singledispatchmethod
    def __eq__(self, a):
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
    def name(self):
        return self._name

    @property
    def short_names(self):
        return self._reverse_interval_distance[self._distance][1:3]



# add note - note = interval to note class
@notes.Note.__sub__.register
def _n1(note1, note2: notes.Note):
    return Interval(note1.distance - note2.distance)


if __name__ == '__main__':
    pass
