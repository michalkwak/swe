class PlayerStats:  # pylint: disable=too-few-public-methods
    def __init__(self, reader):
        self._reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = [
            player for player in self._reader.get_players()
            if player.nationality == nationality
        ]
        return sorted(players, key=lambda player: player.points, reverse=True)

    def top_scorers_by_team(self, team):
        """Return the players who played for the given team (including
        players traded during the season), sorted by points
        in descending order."""
        players = [
            player for player in self._reader.get_players()
            if team in (t.strip() for t in player.team.split(","))
        ]
        return sorted(players, key=lambda player: player.points, reverse=True)

    def top_goal_scorers(self, how_many):
        """Return the how_many players with the most goals,
        sorted by goals in descending order."""
        players = self._reader.get_players()
        by_goals = sorted(
            players, key=lambda player: player.goals, reverse=True
        )
        return by_goals[:how_many]
