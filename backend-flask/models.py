#file for database creation

from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


def drop_and_create_all():
    db.drop_all()
    db.create_all()


class PostModel(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return f"Post(name = {self.name}, description = {self.description}, price = {self.price}, created_at = {self.created_at})"