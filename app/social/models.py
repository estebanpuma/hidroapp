from app import db
from ..admin.models import BaseModel    



class Community(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    
    @staticmethod
    def get_by_id(id):
        return Community.query.filter_by(id = id).first()