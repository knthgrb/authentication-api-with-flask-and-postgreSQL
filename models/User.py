from .. import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    funds = db.relationship("Fund", backref="user")
    
    def __repr__(self):
        return f"User({self.first_name}, {self.last_name}, {self.id})"