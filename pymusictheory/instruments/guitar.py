#!/usr/bin/env python3

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

        # TODO: extract distances_to_tunings as method
        t = []
        if type(tuning) is str:
            t_distances = tunings[strings][tuning]
            for s in t_distances:
                if len(t) > 0:
                    t.append(t[-1]+s)
                else:
                    t.append(notes.Note(root_of_tuning))
        elif type(tuning) is list or type(tuning) is tuple:
            is_strs = True
            is_distances = True
            is_notes = True
            for x in tuning:
                if type(x) is str:
                    is_distance = False
                    is_notes = False
                    t.append(notes.Note(x))
                if type(x) is int:
                    is_strs = False
                    is_notes = False
                    if len(t) > 0:
                        t.append(t[-1]+x)
                    else:
                        t.append(notes.Note(root_of_tuning))
                if type(x) is notes.Note:
                    is_strs = False
                    is_distances = False
                    t.append(notes.Note(x))
            if not is_strs or not is_disance or not is_notes:
                ValueError("Unsupported tuning defintion: Definition must be"
                       + " semitone distance between strings"
                       + " XOR notes.Note for open strings")
        if len(t) != strings:
            raise ValueError('Tuning does not match the amount of strings')

        # fretboard have a distance of semitones = frets + open
        super().__init__(strings, t, [frets+1]*strings)

if __name__ == "__main__":
    pass
