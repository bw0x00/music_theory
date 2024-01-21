#!/bin/env python3

import sys,os

from trallala.instruments.guitar import Guitar
from trallala.core import chords

def main():
    print("\nPrint the fretboard for e standard/ 24 frets")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    # Initialize the Guitar object with 6 Strings, 24 Frets
    # and e-standard tuning
    g = Guitar('e2', tuning='standard', strings=6, frets=24)

    filename = "guitar_fretboard_chord_Cmaj_voicing.svg"

    print("".join((dirname,"/", filename, "> Fretbaord Chord Voicing SVG'" )) )
    with open("/".join((dirname, filename )),'w') as f:
        # create a Cmaj chord
        chord = chords.Chord(chord='major',root='c',voicing=(5,4,4))
        # create svg fretboard with chord
        svg = g.fretboard.svg(chord, root_color="red", notes_color='green')
        # write svg file
        print(svg,file=f)


if __name__ == '__main__':
    main()
