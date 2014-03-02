class ProtonHelper:
    version = "1.0.0"
    def __init__(self, original_input):
        self._input = original_input

    def produce(self, team_scores):
        whole_scores = self.generate_whole_scores(team_scores)
        return {
            "version"      : self.version,
            "match_number" : self._input["match_number"],
            "scores"       : whole_scores,
        }

    def generate_whole_scores(self, team_scores):
        whole = {}
        for tla, team_data in self._input["teams"].items():
            whole[tla] = {
                "zone"          : team_data["zone"],
                "present"       : team_data.get("present", True),
                "disqualified"  : team_data.get("disqualified", False),
                "score"         : team_scores[tla],
            }

        return whole
