#!/usr/bin/env python3

"""
Translation of notes, chords, scales, ... to guitar freboard diagrams.

Supports different amounts of frets, strings and different tunings.

Typical usage examples:
    guitar = Guitar('e2', tuning='standard')
    print(guitar.fretboard.svg(trallala.core.notes.Note('c4')))

"""

import svg

from functools import singledispatchmethod
from textwrap import dedent
from ..core import notes
from ..core import scales
from ..core import chords
from ..core import intervals
from .coreinstruments import _StringedInstrument


tunings = {
        6 : {
            'standard'  : ( 0, 5, 5, 5, 4, 5),
            'drop'      : ( 0, 3, 5, 5, 4, 5)
            }
        }

class Guitar(_StringedInstrument):
    """Guitar class, customizable with parameters

    Attributes:
        fretboard: FretBoard object for SVG output

    """
    def __init__(self,
                 root_of_tuning: notes.Note=notes.Note('e2'),
                 tuning: str='standard', strings: int=6, frets: int=24):
        """ Initializes a Guitar object based on tuning and fretboard

        Args:
            root_of_tuning:
                The lowest note of the used tuning in SPN (default: 'e2')
            tuning:
                str_name of tuning (e.g., standard or drop) or list of
                semitone distances between strings or tuning as notes.Note for
                open strings. (default: 'standard')
            strings:
                amount of strings (default: 6)
            frets:
                amount of frets on the fretboard. (default: 24)
        Raises:
            ValueError: An unsupported tuning was provided
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
        if min(isinstance(x, int) for x in tuning):
            t= []
            for s in tuning:
                if len(t) > 0:
                    t.append(t[-1]+s)
                else:
                    t.append(notes.Note(root))
            return tuple(t)
        if min(isinstance(x, str) for x in tuning):
            tuning = ( notes.Note(x) for x in tuning )
        if min(isinstance(x, notes.Note) for x in tuning):
            t = tuning
            return tuple(t)
        raise ValueError("Unsupported tuning defintion: Definition must be"
                   + " semitone distance between strings"
                   + " XOR notes.Note for open strings")

    @_dispatched_init.register
    def _2(self, tuning: str, root, strings):
        return self._dispatched_init(tunings[strings][tuning], root)

    @property
    def fretboard(self):
        """ Fretboard object of the guitar
        """
        return FretBoard(self._strings,self._tuning,self._frets)


class FretBoard():
    """Representation of the fretboard and definition of the SVG dimensions

    FretBoard provides a parameterizable fretboard supporting SVG output for:
        Scales, Chords, Notes, PitchClasses and Lists of Notes/PitchClasses
    """
    def __init__(self,strings: int, opennotes: tuple, frets: int):
        """ Initializes the fretboard and define the SVG dimensions

        Args:
            strings:
                Amount of strings
            opennotes:
                Value of the open notes defining the tuning.
                len(opennotes) must be equal to strings
            frets:
                Amount of frets
        Property:
            all_notes:
                Multidimensional list with all notes on the fretboard:
                    list[string][fret]
        Raises:
            ValueError: len(opennotes) != strings
        """

        # pylint: disable=too-many-instance-attributes
        # Required to store SVG and fretboard parameters.


        if len(opennotes) != strings:
            raise ValueError("Tuning does not fit amount of strings")
        self._strings = strings
        self._frets = frets

        self._notes = []
        for x in range(strings):
            string = []
            for y in range(frets+1):
                string.append(opennotes[x]+y)
            self._notes.append(string)

        # dimensions for svg fretboard
        # TODO: make fretboard customizable
        self._innerspacing= 20
        self._width = (self._frets+1) * 30 * 2 + 2 * self._innerspacing
        self._height = (self._strings-1) * 15 * 2 + 2 * self._innerspacing
        self._string_distance = (self._height-2*self._innerspacing)/(self._strings-1)
        self._fret_distance   = (self._width -2*self._innerspacing)/(self._frets)
        self._svg_fretboard = self._draw_fretboard()

    @singledispatchmethod
    def get_indices(self, n: notes.Note):
        """ Returns the (y,x) coordinates of n on the fretboard

        Args:
            n:
                List of notes, pitchclasses or single notes, pitchclases,
                scales or chords.
        """
        raise NotImplementedError(f"not implemented for {type(n)}")

    @get_indices.register
    def _1(self, n: notes.Note):
        ret = [] * self._strings
        for s, note_list in enumerate(self._notes):
            for f, note in enumerate(note_list):
                if n == note:
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
            if self._notes[0][0] <= note <= self._notes[-1][-1]:
                ret.append(self.get_indices(note))
        return tuple(ret)

    def __str__(self):
        ret = []
        for s in self._notes:
            ret.append( ", ".join( (str(x) for x in s) ))
        return "\n".join(ret)

    # TODO: move all svg related stuff into output subpackge
    def _draw_fretboard(self) -> svg.SVG:
        """Prints the fretboards as an list of svg elements.
        Must be placed in canvas.
        """
        innerspacing= self._innerspacing
        width = self._width
        height = self._height
        string_distance = self._string_distance
        fret_distance   = self._fret_distance

        fretboard = []
        fretboard.append(svg.Style(text=dedent("""
                            .notebig {font: bold 14px sans-serif; fill: white }
                            .notemedium{font: bold 12px sans-serif; fill: white }
                            .notesmall{font: 8px sans-serif; fill: white }
                            .watermark{font: 8px sans-serif; fill: black }
                                            """)))
        #nut
        fretboard.append(svg.Rect(x=innerspacing-5,y=innerspacing,width=10,
                                  height=height-2*innerspacing,
                                  fill='black', stroke='black'))

        #strings
        for i in range(self._strings):
            y = innerspacing + string_distance * i
            fretboard.append(svg.Line(x1=innerspacing-5,
                                      x2=width-innerspacing+3, y1=y, y2=y,
                                      stroke='black',stroke_width=4))

        #frets
        for i in range(self._frets+1):
            x = innerspacing + fret_distance * i
            fretboard.append(svg.Line(x1=x, x2=x, y1=innerspacing,
                                      y2=height-innerspacing,
                                      stroke='black', stroke_width=6))

        #watermark
        fretboard.append(svg.Text(  x=width-125,
                                    y=height,
                                    class_=['watermark'],
                                    text="Generated with Trallala"))

        return fretboard

    def _draw_notes(self, notes_list, left=False) -> list:
        """Returns svg elements to be added to the fretboard representing the
        notes in "notes". Notes can be a list of notes.Note or
        notes.PitchClass.
        """
        innerspacing= self._innerspacing
        string_distance = self._string_distance
        fret_distance   = self._fret_distance

        notes_svg = []
        for n in notes_list:
            if isinstance(n[0], intervals.Interval):
                i = self.get_indices(notes_list[0][0] + n[0])
            else:
                i = self.get_indices(n[0])
            for (y,x) in i:
                if not left:
                    y = self._strings - (y+1)
                notes_svg.append(svg.Circle(cx=innerspacing+fret_distance*x,
                                            cy=innerspacing+string_distance*y,
                                            r=(string_distance*0.9)/2,
                                            stroke=n[1], stroke_width=1,
                                            fill=n[1] ))
                if len(n[0].name) == 1:
                    notes_svg.append(svg.Text(  x=innerspacing+fret_distance*x-5,
                                                y=innerspacing+string_distance*y+4,
                                                class_=['notebig'],
                                                text=n[0].name.upper(),
                                                fill='white'))
                elif len(n[0].name) == 2:
                    notes_svg.append(svg.Text(  x=innerspacing+fret_distance*x-8,
                                                y=innerspacing+string_distance*y+4,
                                                class_=['notebig'],
                                                text=n[0].name.upper(),
                                                fill='white'))
                elif len(n[0].name) == 6:
                    notes_svg.append(svg.Text(  x=innerspacing+fret_distance*x-11,
                                                y=innerspacing+string_distance*y+3,
                                                class_=['notesmall'],
                                                text=n[0].name.upper().replace("/"
                                                                               ," "),
                                                fill='white'))
                elif len(n[0].name) > 2:
                    notes_svg.append(svg.Text(  x=innerspacing+fret_distance*x-7,
                                                y=innerspacing+string_distance*y+3,
                                                class_=['notebig'],
                                                text=n[0].name.upper(),
                                                fill='white'))
        return notes_svg

    @singledispatchmethod
    def svg(self, n, color: str='green', root_color: str='red',
            notes_color: str='green', intervals: tuple=False) -> svg.SVG:
        """ Creates a fretboard diagram containing n

        Creates an svg fretboard with
        a) a single notes.Note/notes.PitchClass X of color for n=X, color='blue'
        b) a list of notes.Note/notes.PitchClass of colors for n=( (notes.X1, color1),
                                                notes.X2,color2
        c) a chord for n=chords.Chord, root_color=color1, notes_color=color2,
        intervals=False  (default: root_color=red, notes_color=blue)
            If 'intervals' -> output will use Interval names instead of
            PitchClass names
        d) a scale for n=scales.Scale, root_color=color1, notes_color=color2
                (default: red, blue)
                printed in 'root_color', intervalls in 'notes_color'

        Args:
            n:
                Either note, pitchclass (or list of both) or scale or chord.
                In case of list of notes or pitchclasses:
                    The list contains tuple (note/pitchclass,svg_colorname)
            color:
                SVG name of color. Onlye used if n is single note or pitchclass
            root_color:
                SVG name of color used for the root note. Only used if n is
                single chord or scale.
            notes_color:
                SVG name of color used for all other notes. Only used if n is
                sinlge chord or scale.

        """
        fret_diagram = self._svg_fretboard[:]
        fret_diagram.extend(self._draw_notes(n))
        return svg.SVG(width=self._width, height=self._height,
                           elements=fret_diagram)

    @svg.register(notes.Note)
    @svg.register(notes.PitchClass)
    def _1(self, n, color='blue'):
        return self.svg( ((n,color),) )

    @svg.register
    def _2(self, n: chords.Chord, root_color="red", notes_color="green",
           intervals=False):
        n_list = []
        if n.voicing:
            n_list.append( (n[0], root_color) )
            for x in n[1:]:
                if intervals:
                    n_list.append( (x-n[0],notes_color) )
                else:
                    n_list.append( (x,notes_color) )
        else:
            n_list.append( (n.get_pitchclasses()[0], root_color) )
            for x in n[1:]:
                if intervals:
                    n_list.append( (x-n[0],notes_color) )
                else:
                    n_list.append( (notes.PitchClass(x), notes_color) )

        return self.svg(n_list)

    @svg.register
    def _3(self, n: scales.Scale, root_color="red", notes_color="green"):
        n_list = []
        n_list.append( (n[0], root_color) )
        for x in n[1:]:
            n_list.append( (x, notes_color) )
        return self.svg(n_list)

    @property
    def all_notes(self):
        """ All notes.Notes of the fretbaord
        """
        return self._notes

if __name__ == "__main__":
    pass
