#!/bin/env python3

import sys,os
from trallala.core.chords import Chord, chord_integer
from trallala.core.scales import ChromaticScale
from trallala.core.temperament import *

def main():
    print("\nGenerating all scales as defined in " +
          "trallala.chords for standard tuning with " +
          "12TET for the root C4")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]
    root_note = "C"
    octave = 4

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)


    for t in temperament:
        cs = ChromaticScale(temperament=temperament[t])
        for chord in chord_integer[cs.temperament.length]:
            filename = "".join(("standard_tuning_tet12_all_c_chords_",
                                root_note,str(octave),"_", chord,".txt"))
            print("".join((dirname,"/", filename, "> Chord '",root_note,"_", chord  )) )
            with open("/".join((dirname,filename)),'w') as f:
                c = Chord(chord, root_note, chromaticscale=cs)
                print(", ".join( (str(x) for x in c.get_chord()  )  ) ,file=f)

if __name__ == '__main__':
    main()
