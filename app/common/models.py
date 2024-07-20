from app import db
from sqlalchemy.exc import SQLAlchemyError
import os
from flask import current_app
    
class BaseModel():
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
                 
    def __repr__(self):
        return self.name
    
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
    
    def __repr__(self):
        return self.name 
    
    @staticmethod
    def get_by_id(id):
        return Module.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Module.query.filter_by(name=name).first()
    


class Report(db.Model, BaseModel):
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    mod_id = db.Column(db.Integer, db.ForeignKey("modules.id"))
    activity = db.Column(db.String, nullable=False)
    place = db.Column(db.String, nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey("app_users.id"))
    date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time, nullable=False)
    end_hour = db.Column(db.Time, nullable=False)
    total_time = db.Column(db.Float, nullable=False)
    team = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable=False)
    images = db.relationship("ReportImages", cascade='all, delete-orphan')
    notes = db.Column(db.String)
    is_aproved = db.Column(db.Boolean, default=False) 
    module = db.relationship("Module", backref="reports")
    responsible = db.relationship("User")
           
     
class ReportImages(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))
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



