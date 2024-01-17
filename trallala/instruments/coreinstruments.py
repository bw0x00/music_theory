#!/usr/bin/env python3

from ..core import notes

class _Instrument:

    def __init__(self, lowest: notes.Note, highest: notes.Note):
        if lowest > highest:
            raise ValueError("lowest note > highest note")
        self._lowestnote = notes.Note(lowest)
        self._highestnote = notes.Note(highest)

    @property
    def range(self):
        return (self.lowest_note, self.highest_note)

    @property
    def lowest_note(self):
        return notes.Note(self._lowestnote)

    @property
    def highest_note(self):
        return notes.Note(self._highestnote)

class _StringedInstrument(_Instrument):

    def __init__(self, strings, tuning, semitones):
        """
        strings :   amount of strings
        tuning:     list(notes_of_open_string) ordered by string order
        semitones:  list(semitones per string)
        """
        super().__init__(min(tuning),
                         max(tuning)+semitones[tuning.index(max(tuning))]-1)
        self._tuning = tuning
        self._semitones = semitones
        self._strings = strings

    @property
    def semitones(self):
        return self._semitones[:]

    @property
    def tuning(self):
        return self._tuning[:]

    @property
    def strings(self):
        return self._strings


if __name__ == "__main__":
    pass
