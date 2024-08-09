from .. import db
from sqlalchemy.sql import func

class Fund(db.Model):
    __tablename__ = "Funds"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"Fund({self.name}, {self.id})"
    
    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }