#!/usr/bin/env python3

from functools import singledispatchmethod
import svg
from textwrap import dedent
from ..core import notes
from ..core import scales
from ..core import chords
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
        self._strings = strings
        self._frets = frets
        self._notes = []
        for x in range(strings):
            string = []
            for y in range(frets+1):
                string.append(opennotes[x]+y)
            self._notes.append(string)

    def __iter__(self):
        return self._fretboard.__iter__()

    @singledispatchmethod
    def get_indices(self, n):
        """ Returns the (y,x) coordinates of notes, pitchclasses, scales or
        chords
        """
        raise NotImplementedError(f"not implemented for {type(n)}")

    @get_indices.register
    def _1(self, n: notes.Note):
        ret = [] * self._strings
        for s in range(len(self._notes)):
            for f in range(len(self._notes[s])):
                if n == self._notes[s][f]:
                    ret.append( (s,f) )
        return tuple(ret)

    @get_indices.register(notes.PitchClass)
    @get_indices.register(chords.Chord)
    def _2(self, c):
        ret = []
        for note in c:
            ret.extend(self.get_indices(note))
        return tuple(ret)

    @get_indices.register
    def _3(self, n: scales.Scale):
        ret = []
        for note in n:
            if note >= self._notes[0][0] and note <= self._notes[-1][-1]:
                ret.append(self.get_indices(note))
        return tuple(ret)

    def __str__(self):
        ret = []
        for s in self._notes:
            ret.append( ", ".join( (str(x) for x in s) ))
        return "\n".join(ret)

    def _draw_fretboard(self,notes_list: list) -> svg.SVG:
        """
            Prints the fretboards as an svg string.
            a) without paramenters: full fretboard with all notes
            b) with chord:
                - without voicing: all pitchclasses in the chord
                - with voicing: all locations of notes in chord
            c) with pitchclass: all locations of notes from pitchclass
        """
        innerspacing= 20
        width = self._frets * 30 * 2 + 2 * innerspacing
        height = (self._strings-1) * 15 * 2 + 2 * innerspacing

        string_distance = (height-2*innerspacing)/(self._strings-1)
        fret_distance   = (width -2*innerspacing)/(self._frets  -1)

        fretboard = []
        fretboard.append(svg.Style(text=dedent("""
                            .small {font: bold, 20px sans-serif; fill: white }
                                            """)))
        #nut
        fretboard.append(svg.Rect(x=innerspacing-5,y=innerspacing,width=10,
                                  height=height-2*innerspacing,
                                  fill='black', stroke='black'))

        #strings
        for i in range(self._strings):
            y = innerspacing + string_distance * i
            fretboard.append(svg.Line(x1=innerspacing, x2=width-innerspacing, y1=y, y2=y,
                                      stroke='black',stroke_width=5))

        #frets
        for i in range(self._frets):
            x = innerspacing + fret_distance * i
            fretboard.append(svg.Line(x1=x, x2=x, y1=innerspacing,
                                      y2=height-innerspacing,
                                      stroke='black', stroke_width=5))

        for n in notes_list:
            for (y,x) in self.get_indices(n[0]):
                fretboard.append(svg.Circle(cx=innerspacing+fret_distance*x,
                                            cy=innerspacing+string_distance*y,
                                            r=(string_distance*0.9)/2,
                                            stroke=n[1], stroke_width=1,
                                            fill=n[1] ))
                fretboard.append(svg.Text(  x=innerspacing+fret_distance*x-3,
                                            y=innerspacing+string_distance*y+3,
                                            class_=['small'],
                                            text=n[0].name,
                                            fill='white'))


        canvas = svg.SVG(width=width, height=height, elements= fretboard)
        return(str(canvas))

    def svg(self):
        return self._draw_fretboard((   ( notes.PitchClass('e'),'blue'),
                                        ( notes.PitchClass('a#'),'green' ),
                                        ( notes.PitchClass('g'),'red' ) ))

    @property
    def all_notes(self):
        return self._notes

if __name__ == "__main__":
    pass
