from app import db

from app.models import BaseModel, Month


class PmaActivity(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    months = db.relationship("Month", secondary="pma_activity_month", backref="pma_activities")
    
    @staticmethod
    def get_by_id(id):
        return PmaActivity.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(name):
        return PmaActivity.query.filter_by(name=name).first()
    

class PmaActivityMonth(db.Model, BaseModel):
    month_id = db.Column(db.Integer, db.ForeignKey("month.id"), primary_key=True)
    pma_activity_id = db.Column(db.Integer, db.ForeignKey("pma_activity.id"), primary_key=True)
    
    
    