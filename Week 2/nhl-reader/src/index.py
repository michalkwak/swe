import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from player import PlayerReader, PlayerStats

BASE_URL = "https://studies.cs.helsinki.fi/nhlstats"
DEFAULT_SEASON = "2024-25"

console = Console()


def players_table(players, nationality, season):
    table = Table(title=f"Season {season} players from {nationality}")
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


def main():
    season = Prompt.ask("Season (e.g. 2023-24)", default=DEFAULT_SEASON).strip()
    reader = PlayerReader(f"{BASE_URL}/{season}/players")
    stats = PlayerStats(reader)

    try:
        reader.get_players()
    except requests.RequestException as error:
        console.print(f"[bold red]Could not fetch players for {season}:[/bold red] {error}")
        return

    while True:
        nationality = Prompt.ask("Nationality (empty to quit)", default="").strip().upper()
        if not nationality:
            break

        players = stats.top_scorers_by_nationality(nationality)
        if not players:
            console.print(f"[yellow]No players from {nationality} in season {season}[/yellow]")
            continue

        console.print(players_table(players, nationality, season))


if __name__ == "__main__":
    main()
