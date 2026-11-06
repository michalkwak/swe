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
