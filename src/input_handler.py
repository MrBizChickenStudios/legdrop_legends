import pygame
from event_system import event_system

class InputHandler:
    def __init__(self):
        self.control_state = "world"  # 'player', 'menu', or 'battle'
        event_system.on("set_control_state", self.set_control_state)
        event_system.on("get_control_state", self.get_control_state)

    def get_control_state(self):
        return self.control_state

    def set_control_state(self, state):
        self.control_state = state


    def update(self):
        keys = pygame.key.get_pressed()
        key_actions = {
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
            # pygame.K_ESCAPE: "escape",
            pygame.K_RETURN: "action_button",
            pygame.K_p: "set_menu_visible",
        }

        for key, action in key_actions.items():
            if keys[key] and self.control_state == "world":
                self.handle_action(action)


    def handle_action(self, action):
        if self.control_state == "world":
            if action in ("move_up", "move_down", "move_left", "move_right"):
                event_system.raise_event(action)



    def events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)


    def handle_keydown(self, key):
        if self.control_state == "world":
            if key == pygame.K_p:
                event_system.raise_event("set_menu_visible")
            if event_system.raise_event("get_menu_visible")[0]:
                if key == pygame.K_UP:
                    event_system.raise_event("menu_index_up")
                elif key == pygame.K_DOWN:
                    event_system.raise_event("menu_index_down")
                elif key == pygame.K_RETURN:
                    event_system.raise_event("menu_action_button")
                elif key == pygame.K_ESCAPE:
                    event_system.raise_event("menu_back")

        if self.control_state == "battle":
            if key == pygame.K_UP:
                event_system.raise_event("battle_index_up")
            elif key == pygame.K_DOWN:
                event_system.raise_event("battle_index_down")
            elif key == pygame.K_RETURN:
                event_system.raise_event("battle_action_button")
            elif key == pygame.K_ESCAPE:
                event_system.raise_event("battle_back")

        if self.control_state == "dialog":
            if key == pygame.K_UP:
                event_system.raise_event("dialog_index_up")
            elif key == pygame.K_DOWN:
                event_system.raise_event("dialog_index_down")
            elif key == pygame.K_RETURN:
                event_system.raise_event("dialog_enter")
            # elif key == pygame.K_ESCAPE:
            #     event_system.raise_event("dialog_back")

        if self.control_state == "world":
            if key == pygame.K_RETURN:
                event_system.raise_event("action_button_pressed")
        #     elif key == pygame.K_ESCAPE:
        #         event_system.raise_event("dialog_back")





    def handle_keyup(self, key):
        if self.control_state == "world":
            if key == pygame.K_RETURN:
                event_system.raise_event("action_button_released")
