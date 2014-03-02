
import mock

import helpers

helpers.path_bodge()

from proton_helper import ProtonHelper

def assert_load(data_to_load):
    mock_loader = mock.Mock()
    mock_loader.return_value = data_to_load
    ph = ProtonHelper(mock_loader)

    input_ = 'bacon'
    ph.load(input_)

    mock_loader.assert_called_once_with(input_)

    return ph

def test_load():
    loaded_data = {
        "match_number": 1,
        "teams": {
            "TLA1": {
                "zone": 0,
            },
            "TLA2": {
                "zone": 2,
            },
        }
    }

    assert_load(loaded_data)

def test_team_scoresheets():
    teams_data_complete = {
        "TLA1": {
            "zone": 0,
            "bacon": 4,
            "present": True,
            "disqualified": False,
        },
        "TLA2": {
            "zone": 2,
            "bacon": 13,
            "present": False,
            "disqualified": True,
        },
    }
    loaded_data = {
        "match_number": 1,
        "teams": {
            "TLA1": {
                "zone": 0,
                "bacon": 4,
                # defaults
            },
            "TLA2": {
                "zone": 2,
                "bacon": 13,
                "present": False,
                "disqualified": True,
            },
        },
    }

    ph = assert_load(loaded_data)

    team_scoresheets = ph.team_scoresheets

    assert team_scoresheets == teams_data_complete

def test_produce():
    input_ = {
        "match_number": 1,
        "teams": {
            "TLA1": {
                "zone": 0,
            },
            "TLA2": {
                "zone": 2,
                "present": False,
                "disqualified": True,
            },
        }
    }

    mock_loader = mock.Mock()
    mock_loader.return_value = input_
    ph = ProtonHelper(mock_loader)
    ph.load(None)

    scores = { "TLA1": 0, "TLA2": 13 }

    whole = ph.produce(scores)

    assert whole["version"] == "1.0.0"
    assert whole["match_number"] == 1
    assert whole["scores"] == {
        "TLA1": helpers.tla_result_fixture(0, 0),
        "TLA2": {
            "score": 13,
            "zone": 2,
        # while not sane these are expected to be pass-through
            "present": False,
            "disqualified": True,
        },
    }
