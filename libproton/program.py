
from __future__ import print_function

import sys
import traceback
import yaml

from .proton_helper import ProtonHelper


def generate_output(file_reader, scorer_cls, stderr):
    helper = ProtonHelper(yaml.load)

    # Load also validates the input as far as possible
    helper.load(file_reader.read())

    team_scoresheets = helper.team_scoresheets
    arena_data       = helper.arena_data
    extra_data       = helper.extra_data

    scores = None
    try:
        scorer = scorer_cls(team_scoresheets, arena_data)
        scores = scorer.calculate_scores()

        # Also check the validation, if supported. Explicit pre-check so
        # that we don't accidentally hide any AttributeErrors (or similar)
        # which come from inside the method.
        if hasattr(scorer, 'validate'):
            scorer.validate(extra_data)
    except:
        print(traceback.format_exc(), file=stderr)
        exit(2)

    assert scores is not None
    return helper.produce(scores)

def get_reader(args, reader):

    if len(args) == 1:
        # Use the one we were given (stdin)
        return reader

    # Be helpful if we can
    if args[1] in ['-h', '--help']:
        exit("Usage: {} SCORES_YAML".format(args[0]))
    else:
        reader = open(args[1], 'r')

    return reader

def main(scorer, io = sys):
    reader = get_reader(io.argv, io.stdin)
    output = generate_output(reader, scorer, io.stderr)
    yaml.dump(output, io.stdout)
