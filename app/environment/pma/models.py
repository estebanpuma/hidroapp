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
    id = db.Column(db.Integer, primary_key=True)
    month_id = db.Column(db.Integer, db.ForeignKey("month.id"), index=True)
    pma_activity_id = db.Column(db.Integer, db.ForeignKey("pma_activity.id"), index=True)
    year = db.Column(db.Integer, nullable=False)
    
    @staticmethod
    def get_by_act_month_year(activity, month, year):
        return PmaActivityMonth.query.filter_by(pma_activity=activity, month_id=month, year=year).first()
    