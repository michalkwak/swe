import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def __init__(self):
        self.calls = 0  # how many times get_players() has been called

    def get_players(self):
        self.calls += 1
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.reader = PlayerReaderStub()
        self.stats = StatisticsService(self.reader)

    # helper (turn a list of players into a list of their names)
    def names(self, players):
        return [player.name for player in players]

    # constructor

    def test_constructor_reads_players_once_from_reader(self):
        self.assertEqual(self.reader.calls, 1)

    # search

    def test_search_player(self):
        player = self.stats.search("Semenko")

        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.team, "EDM")

    def test_search_with_partial_name(self):
        self.assertEqual(self.stats.search("Gret").name, "Gretzky")

    def test_search_missing_player_returns_none(self):
        self.assertIsNone(self.stats.search("Selanne"))

    # team

    def test_team_returns_players_of_team(self):
        self.assertEqual(
            self.names(self.stats.team("EDM")),
            ["Semenko", "Kurri", "Gretzky"]
        )

    def test_team_contains_only_players_of_team(self):
        for player in self.stats.team("EDM"):
            self.assertEqual(player.team, "EDM")

    def test_team_with_one_player(self):
        self.assertEqual(self.names(self.stats.team("PIT")), ["Lemieux"])

    def test_unknown_team_returns_empty_list(self):
        self.assertEqual(self.stats.team("NYR"), [])

    # top

    def test_top_first_is_best_scorer(self):
        self.assertEqual(self.stats.top(1)[0].name, "Gretzky")

    def test_top_is_sorted_by_points_descending(self):
        self.assertEqual(
            self.names(self.stats.top(3)),
            ["Gretzky", "Lemieux", "Yzerman"]
        )

    def test_top_returns_requested_number_of_players(self):
        self.assertEqual(len(self.stats.top(2)), 2)

    def test_top_zero_returns_empty_list(self):
        self.assertEqual(self.stats.top(0), [])

    def test_top_by_points(self):
        self.assertEqual(
            self.names(self.stats.top(2, SortBy.POINTS)),
            ["Gretzky", "Lemieux"]
        )

    def test_top_by_goals(self):
        self.assertEqual(
            self.names(self.stats.top(2, SortBy.GOALS)),
            ["Lemieux", "Yzerman"]
        )

    def test_top_by_assists(self):
        self.assertEqual(
            self.names(self.stats.top(2, SortBy.ASSISTS)),
            ["Gretzky", "Yzerman"]
        )
