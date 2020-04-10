from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from time import time
import jwt

from flask import current_app
from app import db, login


followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship('User',
            secondary=followers,
            # Указывает условие, которое связывает объект левой стороны
            # (follower user) с таблицей ассоциаций. Условием объединения для
            # левой стороны связи является идентификатор пользователя,
            # соответствующий полю follower_id таблицы ассоциаций.
            # Выражение followers.c.follower_id ссылается на столбец follower_id таблицы ассоциаций.
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            # backref определяет, как эта связь будет доступна из правой части объекта.
            backref=db.backref('followers', lazy='dynamic'),
            lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(followers,
            followers.c.followed_id == Post.user_id).filter(followers.c.follower_id == self.id)
        own = Post.query.filter(Post.user_id == self.id) # Возможная ошибка
        return followed.union(own).order_by(Post.timestamp.desc())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
        current_app.config.get('SECRET_KEY'), algorithm='HS256').decode('utf-8')

    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithm='HS256')['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User %s with id %s>' % (self.username, self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Id post %s of user_id %s >' % (self.id, self.user_id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
