import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

BASE_URL = "https://studies.cs.helsinki.fi/nhlstats"
DEFAULT_SEASON = "2024-25"

console = Console()


def players_table(players, title):
    table = Table(title=title)
    table.add_column("Name", style="cyan")
    table.add_column("Teams", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Points", justify="right", style="bold yellow")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points),
        )

    return table


def load_stats(season):
    reader = PlayerReader(f"{BASE_URL}/{season}/players")

    try:
        reader.get_players()
    except requests.RequestException as error:
        console.print(
            f"[bold red]Could not fetch players for {season}:[/bold red] "
            f"{error}"
        )
        return None

    return PlayerStats(reader)


def show_players(stats, nationality, season):
    players = stats.top_scorers_by_nationality(nationality)
    if not players:
        console.print(
            f"[yellow]No players from {nationality} "
            f"in season {season}[/yellow]"
        )
        return

    console.print(players_table(
        players, f"Season {season} players from {nationality}"
    ))


def show_team_players(stats, team, season):
    players = stats.top_scorers_by_team(team)
    if not players:
        console.print(
            f"[yellow]No players in team {team} "
            f"in season {season}[/yellow]"
        )
        return

    console.print(players_table(
        players, f"Season {season} players of team {team}"
    ))


def main():
    season = Prompt.ask(
        "Season (e.g. 2023-24)", default=DEFAULT_SEASON
    ).strip()
    stats = load_stats(season)
    if stats is None:
        return

    while True:
        mode = Prompt.ask(
            "Search by nationality (n) or team (t), empty to quit",
            choices=["n", "t", ""],
            default="",
            show_choices=False,
        )
        if not mode:
            break
        search(stats, mode, season)


def search(stats, mode, season):
    if mode == "n":
        nationality = Prompt.ask("Nationality").strip().upper()
        show_players(stats, nationality, season)
    else:
        team = Prompt.ask("Team (e.g. BOS)").strip().upper()
        show_team_players(stats, team, season)


if __name__ == "__main__":
    main()
