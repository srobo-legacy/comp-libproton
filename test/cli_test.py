
from __future__ import print_function

import os
import subprocess
import yaml

import helpers

def get_bacon_scorer():
    my_dir = os.path.dirname(os.path.realpath(__file__))
    bacon_scorer = os.path.join(my_dir, 'data/cli/bacon_scorer.py')
    assert os.path.exists(bacon_scorer), bacon_scorer

    return bacon_scorer

def run(relative_path):
    bacon_scorer = get_bacon_scorer()
    process = subprocess.Popen([bacon_scorer,  relative_path], \
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retcode = process.wait()
    return retcode, process

def assert_run(relative_path):
    retcode, process = run(relative_path)
    if retcode != 0:
        print(process.stderr.read())

    assert retcode == 0, "Bad return code scoring '{0}'.".format(relative_path)

    result = process.stdout.read()
    result_dict = yaml.load(result)
    return result_dict

def check_by_input_file(input_name):
    input_file, expected_output = helpers.get_data("test/data/cli", input_name)

    output = assert_run(input_file)

    assert output == expected_output, "Incorrect scores for '{0}'.".format(input_name)

def test_input_file():
    inputs = helpers.get_input_files("test/data/cli")

    for input_name in inputs:
        yield check_by_input_file, input_name

def test_stdin():
    """
    A proton compliant program MUST consume YAML from stdin
    if it is not given a filename.
    """

    zeros_input = open('test/data/cli/zero.yaml', 'r')
    zeros_output = yaml.load(open('test/data/cli/zero.out.yaml').read())

    bacon_scorer = get_bacon_scorer()
    process = subprocess.Popen([bacon_scorer], stdin=zeros_input, \
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retcode = process.wait()
    if retcode != 0:
        print(process.stderr.read())

    assert retcode == 0, "Bad return code scoring from stdin."

    result = process.stdout.read()
    result_dict = yaml.load(result)

    assert result_dict == zeros_output, "Bad output when reading from stdin"

def test_missing_file():
    nope = 'bacon'
    assert not os.path.exists(nope)
    retcode, process = run(nope)
    assert retcode == 1, "Should error when nonexistent input file '{}' is provided.".format(nope)
