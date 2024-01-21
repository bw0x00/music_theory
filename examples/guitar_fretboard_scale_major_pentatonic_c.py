#!/bin/env python3

import sys,os

from trallala.instruments.guitar import Guitar
from trallala.core import scales

def main():
    print("\nPrint the fretboard for e standard/ 12frets")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    # Initialize the Guitar object with 6 Strings, 12 Frets
    # and e-standard tuning
    g = Guitar('e2', tuning='standard', strings=6, frets=12)

    filename = "guitar_fretboard_scale_major_pentatonic_c.svg"

    print("".join((dirname,"/", filename, "> Fretboard Scale SVG'" )) )
    with open("/".join((dirname, filename )),'w') as f:
        # create a major pentatonic
        scale = scales.Scale(scale='major_pentatonic',root='c',)
        # create svg fretboard with scale
        svg = g.fretboard.svg(scale, root_color="red", notes_color='green')
        # write svg file
        print(svg,file=f)


if __name__ == '__main__':
    main()
