#!/usr/bin/env python3

import re
from .definitions import *

##TODO: move to temperament

#def distance_to_note(semitone_distance: dict):
#    reverse_semitone_distance = dict()
#    for k in semitone_distance:
#        if semitone_distance[k] not in reverse_semitone_distance:
#            reverse_semitone_distance[semitone_distance[k]] = [k]
#        else:
#            reverse_semitone_distance[semitone_distance[k]].append(k)
#    return reverse_semitone_distance

#def split_SPN(spn: str):
#	match = re.match(r"([abcdefg][b#]?)([0-9])", spn.lower(), re.I)
#	if match:
#		return match.groups()
#	else:
#		raise ValueError('Bad note name. Note name in SPN required')

if __name__ == "__main__":
    pass
