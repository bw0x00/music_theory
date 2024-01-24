#!/usr/bin/env python3

"""Base modules used for definition of instruments.

Classes in this module should not be used directly.
"""


from ..core import notes



class _Instrument:

    def __init__(self, lowest: notes.Note, highest: notes.Note):
        if lowest > highest:
            raise ValueError("lowest note > highest note")
        self._lowestnote = notes.Note(lowest)
        self._highestnote = notes.Note(highest)

    @property
    def range(self):
        """ Range of the instrument

        Returns:
            Tuple(lowest_note, highest_note)
        """
        return (self.lowest_note, self.highest_note)

    @property
    def lowest_note(self):
        """ Lowest Note of the instrument
        """
        return notes.Note(self._lowestnote)

    @property
    def highest_note(self):
        """ Highest Note of the Instrument
        """
        return notes.Note(self._highestnote)

class _StringedInstrument(_Instrument):

    def __init__(self, strings: int, tuning, semitones: int):
        """ Instanciates a _Stringed Instrument

        args:
            strings:
                amount of strings
            tuning:
                list or tuple(notes_of_open_string) ordered by string order
            semitones:
                list(semitones per string)
        """
        super().__init__(min(tuning),
                         max(tuning)+semitones[tuning.index(max(tuning))]-1)
        self._tuning = tuning
        self._semitones = semitones
        self._strings = strings

    @property
    def semitones(self):
        """ Semitones per string
        """
        return self._semitones[:]

    @property
    def tuning(self):
        """ Tuning of the stringed instrument.

        Tuple containing the open note for each string
        """
        return self._tuning[:]

    @property
    def strings(self):
        """ Amount of strings
        """
        return self._strings


if __name__ == "__main__":
    pass
