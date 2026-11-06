import requests


class Player:
    def __init__(self, data):
        self.name = data['name']
        self.nationality = data['nationality']
        self.team = data['team']
        self.goals = data['goals']
        self.assists = data['assists']

    @property
    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return (
            f"{self.name:22}{self.team:16}"
            f"{self.goals:2} + {self.assists:2} = {self.points}"
        )


class PlayerReader:  # pylint: disable=too-few-public-methods
    def __init__(self, url):
        self._url = url
        self._players = None

    def get_players(self):
        if self._players is None:
            response = requests.get(self._url, timeout=10)
            response.raise_for_status()
            self._players = [
                Player(player_dict) for player_dict in response.json()
            ]
        return self._players


class PlayerStats:  # pylint: disable=too-few-public-methods
    def __init__(self, reader):
        self._reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = [
            player for player in self._reader.get_players()
            if player.nationality == nationality
        ]
        return sorted(players, key=lambda player: player.points, reverse=True)
