import json
import xml.etree.ElementTree as ET
from datetime import datetime

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
        self.posts: list[Post] = []
        self.comments: list[Comment] = []

    def validate(self, username: str, email: str):
        """Валидация пользователя"""
        if not username:
            raise ValidationError("Пользователь не содержит имя")
        if not email:
            raise ValidationError("Пользователь не содержит email")

    def add_post(self, post: 'Post'):
        self.posts.append(post)

    def add_comment(self, comment: 'Comment'):
        self.comments.append(comment)

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Десериализация"""
        user = cls(
            data['user_id'],
            data['username'],
            data['email']
        )
        user.data_registration = datetime.fromisoformat(data['data_registration'])
        return user  # posts и comments восстановятся позже!

    def to_dict(self) -> dict:
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
        self.comments: list[Comment] = []

    def validate(self, text: str):
        """Валидация поста"""
        if not text:
            raise ValidationError("Пост не содержит текст")

    def add_comment(self, comment: 'Comment'):
        self.comments.append(comment)

    @classmethod
    def from_dict(cls, data: dict) -> 'Post':
        """Десериализация"""
        post = cls(
            data['post_id'],
            data['user_id'],
            data['text']
        )
        post.created_at = datetime.fromisoformat(data['created_at'])
        return post  # comments восстановятся позже!

    def to_dict(self) -> dict:
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
    def from_dict(cls, data: dict) -> 'Comment':
        """Десериализация"""
        comment = cls(
            data['comment_id'],
            data['user_id'],
            data['post_id'],
            data['text']
        )
        comment.created_at = datetime.fromisoformat(data['created_at'])
        return comment

    def to_dict(self) -> dict:
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
        self.users: dict[str, User] = {}
        self.posts: dict[str, Post] = {}
        self.comments: dict[str, Comment] = {}

    def add_user(self, user_id: int, username: str, email: str) -> User:
        user = User(user_id, username, email)
        self.users[user_id] = user
        return user

    def add_post(self, post_id: int, user_id: int, text: str) -> Post:
        user = self.users[user_id]
        post = Post(post_id, user_id, text)
        self.posts[post_id] = post
        user.add_post(post)
        return post

    def add_comment(self, comment_id: int, user_id: int, post_id: int, text: str) -> Comment:
        user = self.users[user_id]
        post = self.posts[post_id]
        comment = Comment(comment_id, user_id, post_id, text)
        self.comments[comment_id] = comment
        post.add_comment(comment)
        user.add_comment(comment)
        return comment

    @classmethod
    def from_dict(cls, data: dict) -> 'SocialNetwork':
        """Создание социальной сети из словаря"""
        sn = cls()

        # 1. Создаем все объекты
        for user_data in data.get('users', {}).values():
            user = User.from_dict(user_data)
            sn.users[user.user_id] = user

        for post_data in data.get('posts', {}).values():
            post = Post.from_dict(post_data)
            sn.posts[post.post_id] = post

        for comment_data in data.get('comments', {}).values():
            comment = Comment.from_dict(comment_data)
            sn.comments[comment.comment_id] = comment

        # 2. Восстанавливаем связи
        sn._restore_relationships(data)

        return sn

    def _restore_relationships(self, data: dict):
        """Восстановление всех связей между объектами"""
        # Восстанавливаем комментарии к постам
        for post_id, post_data in data.get('posts', {}).items():
            post = self.posts[int(post_id)]
            for comment_id in post_data.get('comments', []):
                if comment_id in self.comments:
                    post.add_comment(self.comments[comment_id])

        # Восстанавливаем посты пользователей
        for user_id, user_data in data.get('users', {}).items():
            user = self.users[int(user_id)]
            for post_id in user_data.get('posts', []):
                if post_id in self.posts:
                    user.add_post(self.posts[post_id])
            for comment_id in user_data.get('comments', []):
                if comment_id in self.comments:
                    user.add_comment(self.comments[comment_id])

    def to_dict(self) ->dict:
        """Преобразование в словарь для сериализации"""
        return {
            'users': {user_id: user.to_dict() for user_id, user in self.users.items()},
            'posts': {post_id: post.to_dict() for post_id, post in self.posts.items()},
            'comments': {comment_id: comment.to_dict() for comment_id, comment in self.comments.items()}
        }

# Сериализация и десериализация
class SocialNetworkSerializer:
    @staticmethod
    def save_to_json(social_network: SocialNetwork, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(social_network.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"✅ Данные сохранены в {filename}")

    @staticmethod
    def load_from_json(filename: str) -> SocialNetwork:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Данные загружены из {filename}")
        return SocialNetwork.from_dict(data)

    @staticmethod
    def save_to_xml(social_network: SocialNetwork, filename: str):
        root = ET.Element("social_network")

        # Пользователи
        users_elem = ET.SubElement(root, "users")
        for user in social_network.users.values():
            user_elem = ET.SubElement(users_elem, "user")
            user_elem.set("id", str(user.user_id))
            ET.SubElement(user_elem, "username").text = user.username
            ET.SubElement(user_elem, "email").text = user.email
            ET.SubElement(user_elem, "data_registration").text = user.data_registration.isoformat()

        # Посты
        posts_elem = ET.SubElement(root, "posts")
        for post in social_network.posts.values():
            post_elem = ET.SubElement(posts_elem, "post")
            post_elem.set("id", str(post.post_id))
            ET.SubElement(post_elem, "user_id").text = str(post.user_id)
            ET.SubElement(post_elem, "text").text = post.text
            ET.SubElement(post_elem, "created_at").text = post.created_at.isoformat()

        # Комментарии
        comments_elem = ET.SubElement(root, "comments")
        for comment in social_network.comments.values():
            comment_elem = ET.SubElement(comments_elem, "comment")
            comment_elem.set("id", str(comment.comment_id))
            ET.SubElement(comment_elem, "user_id").text = str(comment.user_id)
            ET.SubElement(comment_elem, "post_id").text = str(comment.post_id)
            ET.SubElement(comment_elem, "text").text = comment.text
            ET.SubElement(comment_elem, "created_at").text = comment.created_at.isoformat()

        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"✅ Данные сохранены в {filename}")

def main():
    """Демонстрация работы"""
    try:
        # Создание социальной сети
        sn = SocialNetwork()

        print("=== СОЗДАНИЕ ДАННЫХ ===")
        user1 = sn.add_user(1, "ivan_petrov", "ivan@example.com")
        user2 = sn.add_user(2, "maria_ivanova", "maria@example.com")

        post1 = sn.add_post(101, 1, "Мой первый пост в социальной сети!")
        post2 = sn.add_post(102, 2, "Прекрасный день для прогулки в парке")

        comment1 = sn.add_comment(1001, 2, 101, "Отличный пост!")
        comment2 = sn.add_comment(1002, 1, 102, "Согласен, отличная погода!")

        print(f"Создано: {len(sn.users)} пользователей, {len(sn.posts)} постов, {len(sn.comments)} комментариев")

        print("\n=== СОХРАНЕНИЕ И ЗАГРУЗКА ===")
        # Сохранение
        SocialNetworkSerializer.save_to_json(sn, "social_network_simple.json")
        SocialNetworkSerializer.save_to_xml(sn, "social_network_simple.xml")

        # Загрузка
        sn_loaded = SocialNetworkSerializer.load_from_xml("social_network.xml")
        print(
            f"Загружено: {len(sn_loaded.users)} пользователей, {len(sn_loaded.posts)} постов, {len(sn_loaded.comments)} комментариев")

        # Проверка связей
        user1_loaded = sn_loaded.users[1]
        post1_loaded = sn_loaded.posts[101]
        print(f"У пользователя {user1_loaded.username}: {len(user1_loaded.posts)} постов")
        print(f"У поста {post1_loaded.post_id}: {len(post1_loaded.comments)} комментариев")

        print("\n✅ Всё работает!")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()