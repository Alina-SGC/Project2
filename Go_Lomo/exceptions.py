# exceptions.py

class UserException(Exception):
    """Базовый класс для исключений, связанных с пользователями."""
    pass

class InvalidChatID(UserException):
    """Исключение для неверного chat_id."""
    def __init__(self, chat_id):
        super().__init__(f"Неверный chat_id: {chat_id}. Он должен быть целым числом.")

class InvalidUserState(UserException):
    """Исключение для неверного состояния пользователя."""
    def __init__(self, state):
        super().__init__(f"Неверное состояние пользователя: {state}. Доступные состояния: 'select_place', 'after_info'.")