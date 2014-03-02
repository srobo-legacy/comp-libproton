
import mock
import os
import StringIO
import sys

import helpers

helpers.path_bodge()

import main

@mock.patch('__builtin__.open')
def test_get_reader_file(open_mock):
    mock_default = mock.Mock()
    open_mock.return_value = open_return = mock.Mock()

    file_name = 'bees'
    reader = main.get_reader(['self', file_name], mock_default)

    assert reader is open_return, 'Should have returned the file reader'

    open_mock.assert_called_once_with(file_name, 'r')

@mock.patch('__builtin__.open')
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
            assert "Usage: " in se.message
            assert " self " in se.message

    yield run, '-h'
    yield run, '--help'

def test_inner_error():
    mock_helper_cls = mock.Mock()
    mock_helper = mock.Mock()
    mock_helper_cls.return_value = mock_helper

    mock_reader = mock.MagicMock(spec=file)

    mock_scorer = mock.Mock()
    exception_message = 'Boom!'
    mock_scorer.side_effect = Exception(exception_message)

    with mock.patch('main.ProtonHelper', mock_helper_cls):
        orig_stderr = sys.stderr
        try:
            sys.stderr = StringIO.StringIO()
            main.generate_output(mock_reader, mock_scorer)
            assert False, "Should have exited from inner error"
        except SystemExit as se:
            assert se.code == 2
            output = sys.stderr.getvalue()
            assert 'Traceback' in output
            assert exception_message in output
        finally:
            sys.stderr = orig_stderr
