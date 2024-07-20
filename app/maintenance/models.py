from flask import current_app

from app import db

from app.common.models import BaseModel, Module

from app.common.datetime_format import this_year

import os

from datetime import datetime, time, timedelta


class WorkOrder(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False, unique=True)
    activity = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    status = db.Column(db.String(64), default='Abierta')
    responsible_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    responsible = db.relationship('User', backref='work_orders')
    reports = db.relationship("WorkOrderReport", backref="work_order", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super(WorkOrder, self).__init__(**kwargs)
        self.code = self.generate_code()
        
    @staticmethod
    def generate_code():
        current_year = this_year()
        last_work_order = WorkOrder.query.filter(
            WorkOrder.code.like(f"HID-OT-{current_year}-%")
        ).order_by(WorkOrder.id.desc()).first()
        
        if last_work_order:
            last_code = int(last_work_order.code.split("-")[-1])
            new_code = last_code + 1
        else:
            new_code = 1
    
        return f"HID-OT-{current_year}-{new_code:03d}"


class WorkOrderReport(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey("work_order.id"))
    


class MaintenanceReport(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False)
    workorder_code = db.Column(db.String(128), db.ForeignKey("work_order.code"))
    type = db.Column(db.String(128))
    system = db.Column(db.String(128))
    subsystem = db.Column(db.String(128))
    element = db.Column(db.String(128))
    activity = db.Column(db.Text, nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey("app_users.id"))
    date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time, nullable=False)
    end_hour = db.Column(db.Time, nullable=False)
    total_time = db.Column(db.Float)
    team = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text)
    images = db.relationship("MaintenanceImages", cascade='all, delete-orphan')
    notes = db.Column(db.String) 
    responsible = db.relationship("User")
    
    def __init__(self, **kwargs):
        super(MaintenanceReport, self).__init__(**kwargs)
        self.code = self.generate_code()

    @staticmethod
    def calculate_total_time(start_hour, end_hour):
        start_dt = datetime.combine(datetime.today(), start_hour)
        end_dt = datetime.combine(datetime.today(), end_hour)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)  # Ajuste si el final es al día siguiente
        total_time = (end_dt - start_dt).total_seconds() / 3600  # Convertir a horas
        return total_time
    
    @staticmethod
    def generate_code():
        current_year = this_year()
        last_work_order = WorkOrder.query.filter(
            WorkOrder.code.like(f"HID-MAN-{current_year}-%")
        ).order_by(WorkOrder.id.desc()).first()
        
        if last_work_order:
            last_code = int(last_work_order.code.split("-")[-1])
            new_code = last_code + 1
        else:
            new_code = 1
    
        return f"HID-MAN-{current_year}-{new_code:03d}"
    

class MaintenanceImages(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("maintenance_report.id"))
    filename = db.Column(db.String, unique=True)
    
    def delete(self):
        # Eliminar la imagen física
        if self.filename:
            try:
                image_full_path = os.path.join(current_app.config['REPORT_IMAGES_DIR'], self.filename) 
                os.remove(image_full_path)
                print(f"Image {image_full_path} deleted successfully.")
            except OSError as e:
                print(f"Error deleting image {image_full_path}: {e}")
        
        # Eliminar el registro de la base de datos
        db.session.delete(self)
        db.session.commit()