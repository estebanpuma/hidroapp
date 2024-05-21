from app import db

from app.common.models import BaseModel, Month, Activity

from ...admin.models import User


class PgaActivity(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey("app_users.id"))
    activity = db.relationship("Activity", backref="pga_activities")
    responsible = db.relationship("User", backref="pga_activities")
    months = db.relationship("Month", secondary="pga_activity_month", backref="pga_activities")
    
    @staticmethod
    def get_by_id(id):
        return PgaActivity.query.filter_by(id=id).first()
    
    @staticmethod
    def get_by_name(name):
        return PgaActivity.query.filter_by(name=name).first()
    

class PgaActivityMonth(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    month_id = db.Column(db.Integer, db.ForeignKey("month.id"), index=True)
    pga_activity_id = db.Column(db.Integer, db.ForeignKey("pga_activity.id"), index=True)
    is_done = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer, nullable=False)
    
    @staticmethod
    def get_by_act_month_year(activity, month, year):
        return PgaActivityMonth.query.filter_by(pga_activity=activity, month_id=month, year=year).first()
    