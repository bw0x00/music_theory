#!/usr/bin/env python3

from .definitions import *


def distance_to_note(semitone_distance: dict):
    reverse_semitone_distance = dict()
    for k in semitone_distance:
        if semitone_distance[k] not in reverse_semitone_distance:
            reverse_semitone_distance[semitone_distance[k]] = [k]
        else:
            reverse_semitone_distance[semitone_distance[k]].append(k)
    return reverse_semitone_distance


if __name__ == "__main__":
    pass
