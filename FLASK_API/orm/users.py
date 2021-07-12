import datetime
import sqlalchemy
from .dbsession import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # Id пользователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Имя пользователя
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)  # Почта пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Хэшированный пароль
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # Дата регистрации

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
