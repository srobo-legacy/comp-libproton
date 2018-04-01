
import copy

class ProtonHelper:
    version = "3.0.0-rc2"
    def __init__(self, loader):
        self._loader = loader

    def load(self, input_string):
        self._input = self._loader(input_string)
        self._fill_defaults(self._input['teams'])

    @property
    def team_scoresheets(self):
        return copy.deepcopy(self._input['teams'])

    @property
    def arena_data(self):
        return copy.deepcopy(self._input.get('arena_zones'))

    @property
    def extra_data(self):
        return copy.deepcopy(self._input.get('other'))

    def produce(self, team_scores):
        whole_scores = self.generate_whole_scores(team_scores)
        return {
            "version"      : self.version,
            "match_number" : self._input["match_number"],
            "arena_id"     : self._input["arena_id"],
            "scores"       : whole_scores,
        }

    def _fill_defaults(self, teams_data):
        for team_data in teams_data.values():
            team_data.setdefault("present", True)
            team_data.setdefault("disqualified", False)

    def generate_whole_scores(self, team_scores):
        assert self._input is not None, "Cannot generate whole scores without loading input."
        whole = {}
        for tla, team_data in self._input["teams"].items():
            whole[tla] = {
                "zone"          : team_data["zone"],
                "present"       : team_data["present"],
                "disqualified"  : team_data["disqualified"],
                "score"         : team_scores[tla],
            }

        return whole
