from app import db
from sqlalchemy.exc import SQLAlchemyError


    
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
    def get_by_name(cls, name):
        if cls.name:
            return cls.query.filter_by(name=name).first()
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
    description = db.Column(db.String)
    
    def __repr__(self):
        return self.name 
    
    @staticmethod
    def get_by_id(id):
        return Module.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Module.query.filter_by(name=name).first()
    

    
     
    
     
    