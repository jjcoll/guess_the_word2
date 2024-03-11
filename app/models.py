from app import db
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=True, nullable=False)
    games = db.relationship("Game", backref="game", lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, password_to_check):
        return check_password_hash(self.password_hash, password_to_check)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey("user.username"), nullable=False)
    wordlist = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)
