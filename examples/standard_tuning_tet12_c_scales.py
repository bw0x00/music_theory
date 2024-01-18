#!/bin/env python3

import sys,os
from trallala.core.scales import Scale, scales_steps
from trallala.core.temperament import *
from trallala.core.notes import PitchClass

def main():
    print("\nGenerating all scales as defined in " +
          "trallala.scales for standard tuning with " +
          "12TET")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]
    root_note = "C"
    octave = 4

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    for t in temperament:
        # limit generation to two scales as examples
        for scale in list(scales_steps[temperament[t].length].keys())[0:1]:
            filename = "".join(("standard_tuning_tet12_c_scales_",
                                root_note,str(octave),"_", scale,".txt"))
            print("".join((dirname,"/", filename, "> Scale '",root_note,"_", scale )) )
            with open("/".join((dirname,filename)),'w') as f:
                s = Scale(scale=scale)
                notes = s.get_scale()
                freqs = s.get_scale_frequencies(octave)
                for i in range(len(notes)):
                    print(" : ".join((notes[i].name, str(freqs[i]))),file=f)

if __name__ == '__main__':
    main()
