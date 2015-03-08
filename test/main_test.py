
from __future__ import print_function

import mock
import os
import sys
import yaml

try:
    # python 2, this module's not in python 3
    from StringIO import StringIO
    builtin_open = '__builtin__.open'
except ImportError:
    # python 3, but this module _is_ in python 2 (and behaves differently)
    from io import StringIO
    builtin_open = 'builtins.open'

import helpers

helpers.path_bodge()

import main

@mock.patch(builtin_open)
def test_get_reader_file(open_mock):
    mock_default = mock.Mock()
    open_mock.return_value = open_return = mock.Mock()

    file_name = 'bees'
    reader = main.get_reader(['self', file_name], mock_default)

    assert reader is open_return, 'Should have returned the file reader'

    open_mock.assert_called_once_with(file_name, 'r')

@mock.patch(builtin_open)
def test_get_reader_default(open_mock):
    mock_default = mock.Mock()
    open_mock.return_value = open_return = mock.Mock()

    file_name = 'bees'
    reader = main.get_reader(['self'], mock_default)

    assert reader is mock_default, 'Should have returned the file reader'

    open_mock.assert_no_calls()

def test_get_reader_help():
    def run(arg):
        mock_default = mock.Mock()
        try:
            main.get_reader(['self', arg], mock_default)
            assert False, "Should have exited with usage information"
        except SystemExit as se:
            assert "Usage: " in se.args[0]
            assert " self " in se.args[0]

    yield run, '-h'
    yield run, '--help'

def test_inner_error():
    mock_helper_cls = mock.Mock()
    mock_helper = mock.Mock()
    mock_helper_cls.return_value = mock_helper

    mock_reader = mock.Mock()
    mock_reader.read = mock.Mock(return_value = '')

    mock_scorer = mock.Mock()
    exception_message = 'Boom!'
    mock_scorer.side_effect = Exception(exception_message)

    fake_stderr = StringIO()

    with mock.patch('main.ProtonHelper', mock_helper_cls):
        try:
            main.generate_output(mock_reader, mock_scorer, fake_stderr)
            assert False, "Should have exited from inner error"
        except SystemExit as se:
            assert se.code == 2
            output = fake_stderr.getvalue()
            assert 'Traceback' in output
            assert exception_message in output

# helper for system tests

def run_full_system(input_stream, expected_output):
    mock_io = mock.Mock()
    mock_io.stdout = StringIO()
    mock_io.stderr = StringIO()
    mock_io.stdin = input_stream
    mock_io.argv = ['test']

    def scorer(teams_data):
        return {name: data["zone"] for name, data in teams_data.items()}

    main.main(scorer, io = mock_io)

    print('stdout:\n', mock_io.stdout.getvalue())
    print('stderr:\n', mock_io.stderr.getvalue())
    print(yaml.dump(expected_output))
    output = yaml.load(mock_io.stdout.getvalue())
    assert output == expected_output

def test_system():
    def check_system(data_file):
        data_input, data_output = helpers.get_data("test/data/system",
                                                   data_file)
        with open(data_input) as input_file:
            run_full_system(input_file, data_output)

    for data_file in helpers.get_input_files("test/data/system"):
        yield check_system, data_file
