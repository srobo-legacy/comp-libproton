
from __future__ import print_function

import sys
import traceback
import yaml

from proton_helper import ProtonHelper

def generate_output(file_reader, scorer):
    helper = ProtonHelper(yaml.load)

    # Load also validates the input as far as possible
    helper.load(file_reader.read())

    team_scoresheets = helper.team_scoresheets

    scores = None
    try:
        scores = scorer(team_scoresheets)
    except:
        print(traceback.format_exc(), file=sys.stderr)
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
    output = generate_output(reader, scorer)
    yaml.dump(output, io.stdout)
