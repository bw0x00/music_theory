#!/bin/env python3

import sys,os
import svg
from pymusictheory.instruments.guitar import Guitar
from pymusictheory.core import notes

def main():
    print("\nPrint the fretboard for e standard/ 24frets to stdout")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    filename = "guitar_fretboard_asii_e-standard_6_strings_24frets"
    print("".join((dirname,"/", filename, ".txt> Fretbaord ASCII'" )) )
    with open("/".join((dirname, ".".join( (filename,"txt") ))),'w') as f:
        g = Guitar('e2', tuning='standard', strings=6, frets=24)
        print(str(g.fretboard) ,file=f)

    print("".join((dirname,"/", filename, ".svg> Fretbaord SVG'" )) )
    with open("/".join((dirname, ".".join( (filename,"svg") ))),'w') as f:
        svg = g.fretboard.svg((( notes.PitchClass('e'),'blue'),
                               ( notes.PitchClass('a#'),'green' ),
                               ( notes.PitchClass('g'),'red' )))
        print(svg,file=f)

if __name__ == '__main__':
    main()
