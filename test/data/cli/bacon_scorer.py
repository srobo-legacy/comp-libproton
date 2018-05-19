#!/usr/bin/env python

from os.path import dirname, realpath
import sys

path = dirname(dirname(dirname(dirname(realpath(__file__)))))
sys.path.insert(0, path)

import libproton

class Scorer:
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data

    def calculate_scores(self):
        scores = {}
        for tla, value in self._teams_data.items():
            # Double the bacon and add 5, for fun
            scores[tla] = 5 + 2*value['bacon']
        return scores

    def validate(self, extra_data):
        assert extra_data == 42 or extra_data is None, \
                "Optional extra should be 42 if present"

if __name__ == '__main__':
    libproton.main(Scorer)
