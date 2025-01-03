# decorators.py

def decorate_message(message):
    """
    Декорирует сообщение, добавляя эмодзи и форматирование.
    """
    return f"✨ {message} ✨"

def emphasize(text):
    """
    Подчеркивает текст для выделения.
    """
    return f"*{text}*"

def highlight(text):
    """
    Выделяет текст с помощью символов.
    """
    return f"***{text}***"