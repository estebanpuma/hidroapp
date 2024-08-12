from app import db
from sqlalchemy.exc import SQLAlchemyError
import os
from flask import current_app, flash
from datetime import datetime, timedelta, timezone
from app.utils import this_year

class BaseModel():
    __abstract__ = True
    def save(self):
        print(f"metdo save llamado, self:{self} ")
        try:
            print("intentando guardar")
            db.session.add(self)
            db.session.commit()
            print(f"in method save: {self}")            
            
                
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error occurred while saving: {e}")
            flash("Error al guardar", "warning")

    def delete(self):
        print(f"intentando borrar {self}, {self.id}, ")
        try:
            if self is not None:
                print(f"encontro id {self}")
                db.session.delete(self)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error occurred while deleting: {e}")
            flash("Error al borrar", "warning")
                 
    
    @staticmethod        
    def get_by_id(cls, id):
        if cls.id:
            return cls.query.filter_by(id=id).first()
        else:
            print("error, no existe id")
            
    @staticmethod        
    def get_by_name(self, name):
        if self.name:
            return self.query.filter_by(name=name).first()
        else:
            print("error, no existe")
            

class Month(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    
    def __repr__(self):
        return self.name


class Activity(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String, db.ForeignKey("modules.name") ,nullable = False)
    
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    notes = db.Column(db.String)
    
    @staticmethod
    def get_by_module(module):
        return Activity.query.filter_by(module=module).all()
    

class Module(db.Model, BaseModel):
 
    __tablename__ = "modules"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    code = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    
    reports = db.relationship("Report", back_populates="module")
    work_orders = db.relationship("WorkOrder", back_populates="module")
    
    def __repr__(self):
        return self.name 
    
    @staticmethod
    def get_by_id(id):
        return Module.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Module.query.filter_by(name=name).first()
    
    
class WorkOrder(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False, unique=True)
    activity = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    request_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(64), default='Abierta')
    close_responsible = db.Column(db.String(128))
    notes = db.Column(db.Text)
    priority_level = db.Column(db.String(128))
    
    responsible_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    responsible = db.relationship('User', foreign_keys=[responsible_id], backref='work_orders')
    
    assigned_personnel_id = db.Column(db.Integer, db.ForeignKey('app_users.id'))
    assigned_personnel = db.relationship('User', foreign_keys=[assigned_personnel_id], backref='work_orders_assigned')
    
    
    mod_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    module = db.relationship("Module", back_populates="work_orders")
    
    reports = db.relationship("Report", back_populates="work_order", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super(WorkOrder, self).__init__(**kwargs)
        if not self.mod_id:
            raise ValueError("mod_id is required to create a WorkOrder")
        self.code = self.generate_code()
        
    def generate_code(self):
        mod=Module.query.get_or_404(self.mod_id)
        current_year = this_year()
        
        last_work_order = WorkOrder.query.filter(
            WorkOrder.code.like(f"HID-OT-{mod.code}-{current_year}-%")
        ).order_by(WorkOrder.id.desc()).first()
        
        
        if last_work_order:
            last_code = int(last_work_order.code.split("-")[-1])
            new_code = last_code + 1
        else:
            new_code = 1
    
        return f"HID-OT-{mod.code}-{current_year}-{new_code:03d}"


class Report(db.Model, BaseModel):
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    mod_id = db.Column(db.Integer, db.ForeignKey("modules.id"))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    work_order_id = db.Column(db.Integer, db.ForeignKey("work_order.id"))
    work_order = db.relationship("WorkOrder", back_populates="reports")
    
    module = db.relationship("Module", back_populates="reports")
    details = db.relationship("ReportDetail", back_populates="report", cascade="all, delete-orphan", uselist=False)
    maintenance_details = db.relationship("MaintenanceDetails", back_populates="report", cascade="all, delete-orphan", uselist=False)
    
    @staticmethod
    def generate_code(mod_id):
        mod=Module.query.get_or_404(mod_id)
        current_year = this_year()
        last_report = Report.query.filter(
            Report.code.like(f"HID-{mod.code}-{current_year}-%")
        ).order_by(Report.id.desc()).first()
        
        if last_report:
            last_code = int(last_report.code.split("-")[-1])
            new_code = last_code + 1
        else:
            new_code = 1
    
        return f"HID-{mod.code}-{current_year}-{new_code:03d}"
        

class ReportDetail(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))
    activity = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey("app_users.id"))
    date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time, nullable=False)
    end_hour = db.Column(db.Time, nullable=False)
    total_time = db.Column(db.Float, nullable=False)
    team = db.Column(db.Integer, nullable = False)
    notes = db.Column(db.String)
    is_aproved = db.Column(db.Boolean, default=False) 
    
    report = db.relationship("Report", back_populates="details")
    images = db.relationship("ReportImages", back_populates="report_detail", cascade="all, delete-orphan")
    responsible = db.relationship("User")
    
    @staticmethod
    def calculate_total_time(start_hour, end_hour):
        start_dt = datetime.combine(datetime.today(), start_hour)
        end_dt = datetime.combine(datetime.today(), end_hour)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)  # Ajuste si el final es al día siguiente
        total_time = (end_dt - start_dt).total_seconds() / 3600  # Convertir a horas
        
        return total_time
    
     
class ReportImages(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))
    report_detail_id = db.Column(db.Integer, db.ForeignKey("report_detail.id"))
    filename = db.Column(db.String, unique=True)
    
    report_detail = db.relationship("ReportDetail", back_populates="images")
    
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



class MaintenanceDetails(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    maintenance_type = db.Column(db.String(50))
    element = db.Column(db.String(100))
    system = db.Column(db.String(100))
    subsystem = db.Column(db.String(100))
    
    spare_parts_list = db.relationship("MaintenanceSpareParts", back_populates="maintenance_detail", cascade="all, delete-orphan")
    report = db.relationship("Report", back_populates="maintenance_details")
    

class MaintenanceSpareParts(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    maintenance_detail_id = db.Column(db.Integer, db.ForeignKey("maintenance_details.id"))
    spare_part = db.Column(db.String(100))
    maintenance_detail = db.relationship("MaintenanceDetails", back_populates="spare_parts_list")
   

class ToiletReg(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    hour = db.Column(db.Time)
    place = db.Column(db.String(68))
    notes = db.Column(db.Text)

    img = db.relationship("ToiletRegImg",  cascade="all, delete-orphan")
    
    
class ToiletRegImg(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, db.ForeignKey("toilet_reg.id"))
    filename = db.Column(db.String, unique=True)
    
    def delete(self):
        # Eliminar la imagen física
        if self.filename:
            try:
                image_full_path = os.path.join(current_app.config['TOILET_IMAGES_DIR'], self.filename) 
                os.remove(image_full_path)
                print(f"Image {image_full_path} deleted successfully.")
            except OSError as e:
                print(f"Error deleting image {image_full_path}: {e}")
        
        # Eliminar el registro de la base de datos
        db.session.delete(self)
        db.session.commit()