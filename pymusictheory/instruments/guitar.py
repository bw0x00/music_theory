#!/usr/bin/env python3

from functools import singledispatchmethod
from ..core import notes
from .coreinstruments import _StringedInstrument

tunings = {
    6 : {
        'standard'  : ( 0, 5, 5, 5, 4, 5),
        'drop'      : ( 0, 3, 5, 5, 4, 5)
    }
}

class Guitar(_StringedInstrument):

    def __init__(self, root_of_tuning: notes.Note=notes.Note('e2'), tuning='standard', strings=6, frets=24):
        """
            root_of_tuning: open Note of the lowest string
            tuning: str_name of tuning (e.g., standard or drop) or list of
                semitone distances between strings or tuning as notes.Note for
                open strings
            strings: amount of strings
            frets: amount of frets on the fretboard. Commonly 21 or 24

            Default: E-Standard 6 String Guitar
        """
        t = self._dispatched_init(tuning, root_of_tuning, strings)
        if len(t) != strings:
            raise ValueError('Tuning does not match the amount of strings')

        self._frets = frets
        # fretboard have a distance of semitones = frets + open
        super().__init__(strings, t, [frets+1]*strings)

    @singledispatchmethod
    def _dispatched_init(self, tuning, *args, **kwargs):
        raise ValueError('Unknown tuning')

    @_dispatched_init.register(tuple)
    @_dispatched_init.register(list)
    def _1(self, tuning, root: notes.Note, *args, **kwargs):
        if min([type(x) is int for x in tuning]):
            t= []
            for s in tuning:
                if len(t) > 0:
                    t.append(t[-1]+s)
                else:
                    t.append(notes.Note(root))
            return tuple(t)
        if min([type(x) is str for x in tuning]):
            tuning = ( notes.Note(x) for x in tuning )
        if min([type(x) is notes.Note for x in tuning]):
            t = tuning
            return tuple(t)
        ValueError("Unsupported tuning defintion: Definition must be"
                   + " semitone distance between strings"
                   + " XOR notes.Note for open strings")

    @_dispatched_init.register
    def _2(self, tuning: str, root, strings):
        return self._dispatched_init(tunings[strings][tuning], root)

    @property
    def fretboard(self):
        return FretBoard(self._strings,self._tuning,self._frets)


class FretBoard():

    def __init__(self,strings,opennotes,frets):
        self._notes = []
        for x in range(strings):
            string = []
            for y in range(frets+1):
                string.append(opennotes[x]+y)
            self._notes.append(string)

    def __iter__(self):
        return self._fretboard.__iter__()

    @property
    def all_notes(self):
        return self._notes

if __name__ == "__main__":
    pass
