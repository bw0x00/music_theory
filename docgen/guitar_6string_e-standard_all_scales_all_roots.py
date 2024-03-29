#!/bin/env python3

import sys,os
from trallala.core.scales import Scale, scales_steps
from trallala.core.temperament import *
from trallala.core.notes import PitchClass
from trallala.instruments.guitar import Guitar

def main():
    print("\nGenerating all scales as defined in " +
          "trallala.scales for e-standard ")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    t=12
    g = Guitar()

    for scale in scales_steps[t]:
        for root_numeric in range(t):
            pc = PitchClass(root_numeric)
            filename = "".join(("scale_guitar_",pc.name,"_", scale,".svg"))
            print("".join((dirname,"/", filename, "> Scale '",pc.name,"_", scale )) )
            with open("/".join((dirname,filename)),'w') as f:
                s = Scale(root=pc, scale=scale)
                svg = g.fretboard.svg( s )
                print(svg,file=f)

if __name__ == '__main__':
    main()
