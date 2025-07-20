import pygame
from constants import *
from  battle.battle_graphics import BattleGraphics
import battle.enemy_ai
from player.player import main_player
from battle.player_actions import PlayerActions
from  battle import message_display
from event_system import event_system
import copy

class Battle():
    def __init__(self, enemy):
        event_system.raise_event("player_set_in_dialog", False)
        event_system.raise_event("set_control_state", "battle")
        self.message_display = message_display.MessageDisplay()
        self.player_actions = PlayerActions(self)

        self.enemy = enemy.battle_object
        self.enemy.rect.topleft = (700, 20)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)
        self.player_group = pygame.sprite.Group()

        self.index = 0

        self.stable = []
        for wrestler in main_player.stable:
            self.stable.append({"wrestler" : wrestler})

        print(self.stable)

        self.current_wrestler = self.stable[1]["wrestler"].battle_object
        self.current_wrestler.rect.topleft = (0, 300)
        print(f"current wrestler: {self.current_wrestler}")
        self.player_group.add(self.current_wrestler)


        self.extra_options = {
            "Items": [
                {"name": "Bandaid", "hp": 5, "type": "restore_hp", "qty": 5, "message": f" used Bandaid"},
                {"name": "Beer", "mp": 30, "type": "restore_mp", "qty": 5, "message": f" used Beer"},
                {"name": "Powder", "mp": 5, "type": "restore_mp", "qty": 5, "message": f" powered"},
            ],
            "Tag Partner": [
                {"name": wrestler["wrestler"].battle_object.name, "type": "tag", "index": i}
                for i, wrestler in enumerate(self.stable)
                ],

            "Powder": [
                {"name": "Powder", "mp": 0, "type": "restore_mp", "message": ""},
            ],
            "Run": [
                {"name": "Run", "type": "run", "message": "Player tried running"},
            ]
        }


        # print(main_player.stable)

        self.battle_options = copy.deepcopy(self.current_wrestler.options)
        self.battle_options.update(self.extra_options)
        self.current_menu = list(self.battle_options.keys())
        self.in_submenu = False
        self.parrent_menu = None
        self.turn = "player"
        self.can_enemy_turn = False
        self.turn_delay = 3000
        self.shake_delay = 500

        self.is_start_of_turn = True
        self.battle_graphics = BattleGraphics(self)

        self.enemy_ai = battle.enemy_ai.EnemyAI(self.enemy, self)
        self.has_controls = True
        self.has_player_died = False
        self.has_enemy_died = False

        event_system.on("battle_index_up", self.index_up)
        event_system.on("battle_index_down", self.index_down)
        event_system.on("battle_action_button", self.action_button)
        event_system.on("battle_back", self.back)


        self.current_menu = list(self.battle_options.keys())
        self.index = 0
        self.in_submenu = False
        self.parent_menu = None

    def switch_wrestler(self, wrestler):
        self.player_group.remove(self.current_wrestler)
        self.current_wrestler = wrestler
        self.player_group.add(self.current_wrestler)
        self.battle_options = copy.deepcopy(self.current_wrestler.options)
        self.battle_options.update(self.extra_options)
        self.current_menu = list(self.battle_options.keys())
        self.index = 0
        self.in_submenu = False
        self.parent_menu = None
        self.current_wrestler.rect.topleft = (0, 300)
        self.message_display.set_message(f"{self.current_wrestler.name} was tagged in.")



    def reset(self):
        self.enemy.reset()
        self.current_wrestler.reset()

        # 🚨 RESET ALL MENU NAVIGATION STATE
        self.current_menu = list(self.battle_options.keys())
        self.index = 0
        self.in_submenu = False
        self.parent_menu = None

    # ✅ Leave battle state and return to world
        event_system.raise_event("change_to_parent_state")
        event_system.raise_event("set_control_state", "world")
    def update(self):
        self.player_group.update()
        self.enemy_group.update()
        self.message_display.update()
        self.enemy.update()
        self.current_wrestler.update()
        self.enemy_ai.update()



        if self.current_wrestler.hp <= 0 and not self.has_player_died:
            self.has_player_died = True
            self.player_actions.player_died()
            self.has_controls = False

        if self.enemy.hp <= 0 and not self.has_enemy_died:
            self.has_enemy_died = True
            self.player_actions.enemy_died()
            self.has_controls = False

        # self.index = max(0, min(self.index, len(self.current_menu) - 1))
        if self.turn == "enemy" and not self.has_enemy_died:
            self.enemy_ai.enemy_turn()


    def draw(self, surface):
        self.battle_graphics.draw(surface)
        self.enemy_group.draw(surface)
        self.player_group.draw(surface)


    def set_player_turn(self):
        self.has_controls = True
        self.turn = "player"


    def events(self, events):
        pass


    def index_up(self):
        if self.has_controls:
            self.index -= 1


    def index_down(self):
        if self.has_controls:
            self.index += 1

    def back(self):
        self.current_menu = self.parent_menu
        self.index = 0
        self.in_submenu = False

    def action_button(self):
        self.index = max(0, min(self.index, len(self.current_menu) - 1))

        if self.has_controls:
            key = self.current_menu[self.index]
            if not self.in_submenu:
                submenu_data = self.battle_options[key]
                if isinstance(submenu_data, list):
                    self.parent_menu = self.current_menu
                    self.current_menu = submenu_data

                    self.in_submenu = True
                    self.index = 0
            # if isinstance(key, dict):
            #     if key["name"] == "Back":
            #         self.current_menu = self.parent_menu
            #         self.index = 0
            #         self.in_submenu = False
            #     else:
            self.player_actions.action(key)
