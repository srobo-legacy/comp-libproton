# LibProton

[![Build Status](https://travis-ci.org/PeterJCLaw/libproton.png)](https://travis-ci.org/PeterJCLaw/libproton)

This is a library which simplifies the task of creating
[Proton](https://github.com/samphippen/proton) compliant scoring scripts.

It supports Python 2.7 and 3.x.

## API

The following is a complete and minimal Proton compliant scorer, and shows
the expected usage of the library.

~~~~
#!/usr/bin/env python

import libproton

def scorer(teams_data):
    # Whatever you need to do to work out the team's scores
    scores = {}
    for tla in teams_data.keys():
        scores[tla] = 4
    return scores

libproton.main(scorer)
~~~~

## Tests
Run `nosetests` from the root.
