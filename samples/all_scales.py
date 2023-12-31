#!/bin/env python3

import sys,os
from pymusictheory.scales import Scale
from pymusictheory.definitions import *

def main():
    print("Generating all scales as defined in " +
          "pymusictheory.definitions.scales_steps")
    print("Writing output into folder: " + sys.argv[1])

    dirname = sys.argv[1]
    root_note = "C"

    if not os.path.isdir(dirname):
        print("Output dir does not exist: " + dirname)

    for temperament in scales_steps:
        for scale in scales_steps[temperament]:
            filename = "".join(("scale_",root_note,"_", scale,".txt"))
            print("".join(("> Scale '",root_note,"_", scale, "': ", dirname,"/",filename )) )
            try:
                f = open("/".join((dirname,filename)),'w') 
            except Exception as e:
                print("Cannot open file " + "/".join((dirname,filename)) )
                raise e

if __name__ == '__main__':
    main()
