# LibProton

[![Build Status](https://travis-ci.org/PeterJCLaw/libproton.png)](https://travis-ci.org/PeterJCLaw/libproton)

This is a library which simplifies the task of creating
[Proton](https://github.com/samphippen/proton) compliant scoring scripts.

It supports Python 2.7 and 3.x.

## API

The following is a complete and minimal Proton compliant scorer, and shows
the expected usage of the library.

~~~~ .python
#!/usr/bin/env python

import libproton

class Scorer:
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def calculate_scores(self):
        """Main scoring entry point.

           Expected to return a mapping of TLA -> score for each team in
           the input data. Errors either in the input or otherwise should
           be handled by raising exceptions.
        """
        scores = {}
        for tla in self._teams_data.keys():
            scores[tla] = 4
        return scores

    def validate(self, extra_data):
        """An optional additional method to validate the scoresheet.

           If this method is implemented it will be called with the value
           of the ``other`` key from the input. If the key is not present
           then this method will still be called (with ``None``).

           If there are validation errors the this method should raise
           an exception about them.
        """
        pass

libproton.main(Scorer)
~~~~

## Tests
Run `nosetests` from the root.
