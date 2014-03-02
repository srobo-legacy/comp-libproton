
import os
import sys
import yaml

import helpers

path = os.path.dirname(os.path.realpath(__file__)) + "/../lib/"
sys.path.insert(0, path)
print sys.path

from proton_helper import ProtonHelper

def test_proton_helper():
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

    ph = ProtonHelper(input_)

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
