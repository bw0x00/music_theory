#!/bin/env python3

import sys,os
from pymusictheory.scales import Scale, scales_steps
from pymusictheory.temperament import *

def main():
    print("\nGenerating all scales as defined in " +
          "pymusictheory.scales for standard tuning with " +
          "12TET")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]
    root_note = "C"
    octave = 4

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    for t in temperament:
        for scale in scales_steps[temperament[t].length]:
            filename = "".join(("scale_",root_note,str(octave),"_", scale,".txt"))
            print("".join(("> Scale '",root_note,"_", scale, "': ", dirname,"/",filename )) )
            with open("/".join((dirname,filename)),'w') as f:
                s = Scale(scale=scale)
                notes = s.get_scale()
                freqs = s.get_scale_frequencies(octave)
                for i in range(len(notes)):
                    print(" : ".join((",".join(notes[i]),str(freqs[i]))),file=f)

if __name__ == '__main__':
    main()
