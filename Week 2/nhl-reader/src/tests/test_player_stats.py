import socket
import unittest
from unittest import mock

from player import Player
from player_stats import PlayerStats


PLAYER_FIELDS = ("name", "nationality", "team", "goals", "assists")


def make_player(*values):
    return Player(dict(zip(PLAYER_FIELDS, values)))


class PlayerReaderStub:  # pylint: disable=too-few-public-methods
    """Stands in for PlayerReader and returns fixed players without
    any network access."""

    def __init__(self, players):
        self._players = players

    def get_players(self):
        return self._players


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        # Fail loudly if anything tries to open a network connection.
        patcher = mock.patch.object(
            socket, "socket",
            side_effect=AssertionError("tests must not use the network"),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.players = [
            make_player("Semenko", "FIN", "EDM", 4, 12),
            make_player("Lemieux", "CAN", "PIT", 45, 54),
            make_player("Kurri", "FIN", "EDM", 37, 53),
            make_player("Yzerman", "CAN", "DET", 42, 56),
            make_player("Gretzky", "CAN", "EDM, LAK", 35, 89),
        ]
        self.stats = PlayerStats(PlayerReaderStub(self.players))

    @staticmethod
    def names(players):
        return [player.name for player in players]

    def test_by_nationality_returns_only_that_nationality(self):
        result = self.stats.top_scorers_by_nationality("FIN")
        self.assertEqual(self.names(result), ["Kurri", "Semenko"])

    def test_by_nationality_sorted_by_points_descending(self):
        result = self.stats.top_scorers_by_nationality("CAN")
        self.assertEqual(
            self.names(result), ["Gretzky", "Lemieux", "Yzerman"]
        )

    def test_by_nationality_unknown_returns_empty_list(self):
        self.assertEqual(self.stats.top_scorers_by_nationality("SWE"), [])

    def test_by_team_sorted_by_points_descending(self):
        result = self.stats.top_scorers_by_team("EDM")
        self.assertEqual(
            self.names(result), ["Gretzky", "Kurri", "Semenko"]
        )

    def test_by_team_includes_traded_players(self):
        result = self.stats.top_scorers_by_team("LAK")
        self.assertEqual(self.names(result), ["Gretzky"])

    def test_by_team_does_not_match_partial_team_code(self):
        self.assertEqual(self.stats.top_scorers_by_team("ED"), [])

    def test_by_team_unknown_returns_empty_list(self):
        self.assertEqual(self.stats.top_scorers_by_team("BOS"), [])

    def test_top_goal_scorers_sorted_by_goals_descending(self):
        result = self.stats.top_goal_scorers(3)
        self.assertEqual(
            self.names(result), ["Lemieux", "Yzerman", "Kurri"]
        )

    def test_top_goal_scorers_more_than_available_returns_all(self):
        self.assertEqual(len(self.stats.top_goal_scorers(10)), 5)

    def test_top_goal_scorers_zero_returns_empty_list(self):
        self.assertEqual(self.stats.top_goal_scorers(0), [])
