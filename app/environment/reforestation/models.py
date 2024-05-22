from app.common.models import BaseModel
from app.admin.models import User

from app import db


class Plant(db.Model, BaseModel):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return self.name
    
