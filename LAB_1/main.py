# Базовые исключения
class SocialNetworkError(Exception):
    """Базовое исключение для социальной сети"""
    pass

class UserNotFoundError(SocialNetworkError):
    """Пользователь не найден"""
    pass

class PostNotFoundError(SocialNetworkError):
    """Пост не найден"""
    pass

class FriendshipError(SocialNetworkError):
    """Ошибка дружбы"""
    pass

class ValidationError(SocialNetworkError):
    """Ошибка валидации данных"""
    pass


class User:
    def __init__(self, name):
        pass

class Post:
    def __init__(self, text):
        pass

class Comment:
    def __init__(self, text):
        pass

class SocialNetwork:
    def __init__(self):
        pass

# Сериализация и десериализация
class SocialNetworkSerializer:
    def __init__(self):
        pass

def main():
    pass