# user.py
from exceptions import InvalidChatID, InvalidUserState

class User:
    def __init__(self, chat_id):
        if not isinstance(chat_id, int):
            raise InvalidChatID(chat_id)  # Вызываем исключение, если chat_id неверный
        self.chat_id = chat_id
        self.state = 'start'

    def reset_state(self):
        self.state = 'start'

    def set_state(self, new_state):
        if new_state not in ['select_place', 'after_info']:
            raise InvalidUserState(new_state)  # Вызываем исключение, если состояние неверное
        self.state = new_state

    def get_state(self):
        return self.state