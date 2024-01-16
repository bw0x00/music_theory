#!/bin/env python3

import sys,os
import svg
from pymusictheory.instruments.guitar import Guitar
from pymusictheory.core import notes
from pymusictheory.core import chords
from pymusictheory.core import scales

def main():
    print("\nPrint the fretboard for e standard/ 24frets to stdout")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    g = Guitar('e2', tuning='standard', strings=6, frets=24)
    filename = "guitar_fretboard_asii_e-standard_6_strings_24frets"

    print("".join((dirname,"/", filename, ".txt> Fretbaord ASCII'" )) )
    with open("/".join((dirname, ".".join( (filename,"txt") ))),'w') as f:
        print(str(g.fretboard) ,file=f)

    print("".join((dirname,"/", filename, ".svg> Fretbaord PitchClasses SVG'" )) )
    with open("/".join((dirname, "".join( (filename,"_pitchclasses",".svg") ))),'w') as f:
        svg = g.fretboard.svg((( notes.PitchClass('e'),'blue'),
                               ( notes.PitchClass('a#'),'green' ),
                               ( notes.PitchClass('g'),'red' )))
        print(svg,file=f)

    x = "_single_note"
    print("".join((dirname,"/", filename,x, ".svg> Fretbaord Single Note SVG'" )) )
    with open("/".join((dirname, "".join( (filename,x ,".svg") ))),'w') as f:
        svg = g.fretboard.svg(notes.Note('e4'),color="green")
        print(svg,file=f)

    x = "_single_pitchclass"
    print("".join((dirname,"/", filename, x, ".svg> Fretbaord Single PitchClass SVG'" )) )
    with open("/".join((dirname, "".join( (filename, x,".svg") ))),'w') as f:
        svg = g.fretboard.svg(notes.PitchClass('a#'),color="red")
        print(svg,file=f)

    x = "_chord_Cmaj"
    print("".join((dirname,"/", filename, x, ".svg> Fretbaord Chord SVG'" )) )
    with open("/".join((dirname, "".join( (filename, x,".svg") ))),'w') as f:
        svg = g.fretboard.svg(chords.Chord(chord='major',root='c',voicing=(3,3,3)),
                                            root_color="red", notes_color='green')
        print(svg,file=f)

    x = "_chord_Cmaj_pitchclasses"
    print("".join((dirname,"/", filename, x, ".svg> Fretbaord Chord->PitchClasses SVG'" )) )
    with open("/".join((dirname, "".join( (filename, x,".svg") )))
                ,'w') as f:
        svg = g.fretboard.svg(chords.Chord(chord='major',root='c'),
                                            root_color="red", notes_color='green')
        print(svg,file=f)

    x = "_scale_c_major_pentatonic"
    print("".join((dirname,"/", filename, x, ".svg> Fretbaord C major Pentatonic SVG'" )) )
    with open("/".join((dirname, "".join( (filename, x,".svg") )))
                ,'w') as f:
        svg = g.fretboard.svg(scales.Scale(scale='major_pentatonic',root='c'),
                                            root_color="red",
                                            notes_color='green')
        print(svg,file=f)


if __name__ == '__main__':
    main()
