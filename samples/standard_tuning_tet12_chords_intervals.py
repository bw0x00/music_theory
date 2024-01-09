#!/bin/env python3

import sys, os, json
from pymusictheory.core.chords import Chord, chord_integer
from pymusictheory.core.scales import ChromaticScale
from pymusictheory.core.temperament import *
from pymusictheory.core.intervals import Interval

chords = {
        'major6'            : ('root', 'M3', 'P5', 'M6'),
        'major7'            : ('root', 'M3', 'P5', 'M7'),
        'major9'            : ('root', 'M3', 'P5', 'M7', 'M9'),
        'major11'           : ('root', 'M3', 'P5', 'M7', 'M9', 'P11'),
        'major13'           : ('root', 'M3', 'P5', 'M7', 'M9', 'P11', 'M13'),
        'sus2'              : ('root', 'M2', 'P5'),
        'sus4'              : ('root', 'P4', 'P5'),
        'dominant7'         : ('root', 'M3', 'P5', 'm7'),
        'dominant9'         : ('root', 'M3', 'P5', 'm7', 'M9'),
        'dominant11'        : ('root', 'M3', 'P5', 'm7', 'M9', 'P11'),
        'dominant13'        : ('root', 'M3', 'P5', 'm7', 'M9', 'P11', 'M13'),
        'minor6'            : ('root', 'm3', 'P5', 'M6'),
        'minor7'            : ('root', 'm3', 'P5', 'm7'),
        'minorM7'           : ('root', 'm3', 'P5', 'M7'),
        'minor9'            : ('root', 'm3', 'P5', 'm7','M9'),
        'minor11'           : ('root', 'm3', 'P5', 'm7','M9', 'P11'),
        'diminished'        : ('root', 'm3', 'd5'),
        'diminished7'       : ('root', 'm3', 'd5', 'd7'),
        'half_diminished7'  : ('root', 'm3', 'd5', 'm7'),
        'augmented'         : ('root', 'M3', 'A5'),
        'augmented7'        : ('root', 'M3', 'A5', 'm7'),
        'dominant7sus4'     : ('root', 'P4', 'P5', 'm7')
    }

def main():
    print("\nGenerating chords from Intervals " +
          "for standard tuning with " +
          "12TET for the root C4")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]
    root_note = "C"
    octave = 4

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)


    for t in temperament:
        cs = ChromaticScale(temperament=temperament[t])
        filename = "".join(("chords_int_from_intervals.txt"))
        with open("/".join((dirname,filename)),'w') as f:
            out = dict()
            for chord in chords:
                print("".join((dirname,"/",filename,
                               "> '",root_note,"_", chord, "'")) )
                i = [Interval(x) for x in chords[chord]]
                c = Chord(i, root_note, chromaticscale=cs )
                out[chord] = c.chord_int
            print(json.dumps(out),file=f)

if __name__ == '__main__':
    main()
