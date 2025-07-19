from states.state import State
from states import state
from battle.battle import Battle
from event_system import event_system

class BattleState(State):
    def __init__(self, enemy):
        self.enemy = enemy
        self.battle = Battle(self.enemy)
        self.state_name = "battle"
        self.song_file = enemy.song_file
        event_system.raise_event("music_manager_play", self.song_file)
    def events(self, events):
        self.battle.events(events)

    def update(self):
        self.battle.update()

    def draw(self, surface):
        self.battle.draw(surface)
