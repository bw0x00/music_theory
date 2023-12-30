#!/usr/bin/env python3

from .definitions import *


def distance_to_note(tone_distance: dict):
    reverse_tone_distance = dict()
    for k in tone_distance:
        if tone_distance[k] not in reverse_tone_distance:
            reverse_tone_distance[tone_distance[k]] = [k]
        else:
            reverse_tone_distance[tone_distance[k]].append(k)
    return reverse_tone_distance


if __name__ == "__main__":
    pass
