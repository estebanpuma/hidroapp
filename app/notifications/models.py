from app import db
from app.common.models import BaseModel
from app.utils import get_current_time_quito


class Notification(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=True)
    wo_id = db.Column(db.Integer, db.ForeignKey('work_order.id'), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=get_current_time_quito)
    
    user_notifications = db.relationship('UserNotification', back_populates='notification')
   
class UserNotification(db.Model, BaseModel):
    __tablename__ = 'user_notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_users.id'), nullable=False)
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    is_checked = db.Column(db.Boolean, default=False)
    
    notification = db.relationship('Notification', back_populates='user_notifications')
    recipients = db.relationship('User',  back_populates='notifications')