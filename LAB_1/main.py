from datetime import datetime
from typing import Dict, List

# Базовые исключения
class SocialNetworkError(Exception): pass
class UserNotFoundError(SocialNetworkError): pass
class PostNotFoundError(SocialNetworkError): pass
class ValidationError(SocialNetworkError): pass


class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.validate(username, email)

        self.user_id = user_id
        self.username = username
        self.email = email
        self.data_registration = datetime.now()
        self.post: List[Post] = []
        self.comment: List[Comment] = []

    def validate(self, username: str, email: str):
        """Валидация пользователя"""
        if not username:
            raise ValidationError("Пользователь не содержит имя")
        if not email:
            raise ValidationError("Пользователь не содержит email")

    def add_post(self, post: 'Post'):
        self.post.append(post)

    def add_comment(self, comment: 'Comment'):
        self.comment.append(comment)

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Десериализация"""
        user = cls(
            data['user_id'],
            data['username'],
            data['email']
        )
        user.data_registration = datetime.fromisoformat(data['data_registration'])
        return user  # posts и comments восстановятся позже!

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'data_registration': self.data_registration.isoformat(),
            'posts': [p.post_id for p in self.posts],
            'comments': [c.comment_id for c in self.comments]
        }

    def __str__(self):
        return f"User({self.user_id}): {self.username}"


class Post:
    def __init__(self, post_id: int, user_id: int, text: str):
        self.validate(text)

        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.created_at = datetime.now()
        self.comment: List[Comment] = []

    def validate(self, text: str):
        """Валидация поста"""
        if not text:
            raise ValidationError("Пост не содержит текст")

    def add_comment(self, comment: 'Comment'):
        self.comment.append(comment)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Post':
        """Десериализация"""
        post = cls(
            data['post_id'],
            data['user_id'],
            data['text']
        )
        post.created_at = datetime.fromisoformat(data['created_at'])
        return post  # comments восстановятся позже!

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'comments': [c.comment_id for c in self.comments]
        }

    def __str__(self):
        text_preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Post({self.post_id}): {text_preview}"

class Comment:
    def __init__(self, comment_id: int, user_id: int, post_id: int, text: str):
        self.validate(text)

        self.comment_id = comment_id
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.created_at = datetime.now()

    def validate(self, text: str):
        """Валидация комментария"""
        if not text:
            raise ValidationError("Комментарии не содержат текст")

    @classmethod
    def from_dict(cls, data: Dict) -> 'Comment':
        """Десериализация"""
        comment = cls(
            data['comment_id'],
            data['user_id'],
            data['post_id'],
            data['text']
        )
        comment.created_at = datetime.fromisoformat(data['created_at'])
        return comment

    def to_dict(self) -> Dict:
        """Преобразование в словарь для сериализации"""
        return {
            'comment_id': self.comment_id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'text': self.text,
            'created_at': self.created_at.isoformat()
        }

    def __str__(self):
        return f"Comment({self.comment_id}): {self.text[:30]}..."


class SocialNetwork:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.posts: Dict[str, Post] = {}

# Сериализация и десериализация
class SocialNetworkSerializer:
    pass

def main():
    pass