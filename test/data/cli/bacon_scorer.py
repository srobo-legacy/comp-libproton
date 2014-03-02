#!/usr/bin/env python

from os.path import dirname, realpath
import sys

path = dirname(dirname(dirname(dirname(realpath(__file__)))))
sys.path.insert(0, path)

import libproton

def scorer(teams_data):
    scores = {}
    for tla, value in teams_data.items():
        # Double the bacon and add 5, for fun
        scores[tla] = 5 + 2*value['bacon']
    return scores

libproton.main(scorer)
