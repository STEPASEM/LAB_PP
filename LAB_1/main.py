from datetime import datetime

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
    def __init__(self, user_id: int, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.data_registration = datetime.now()
        self.post: list[Post] = []
        self.comment: list[Comment] = []


class Post:
    def __init__(self, post_id: int, user_id: int, text: str):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.created_at = datetime.now()
        self.comment: list[Comment] = []

class Comment:
    def __init__(self, comment_id: int, user_id: int, post_id: int, text: str):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.created_at = datetime.now()


class SocialNetwork:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.posts: dict[str, Post] = {}

# Сериализация и десериализация
class SocialNetworkSerializer:
    pass

def main():
    pass