from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db 
from app.models import BaseModel



class User(db.Model, UserMixin, BaseModel):
    
    __tablename__ = "app_users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), default=1)
    birth = db.Column(db.Date)
    role = db.relationship("Role")
    
    def __repr__(self):
        return self.name

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        query = User.query.filter_by(email = email).first()
        return query or None
    

class Role(db.Model, BaseModel):
    
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    permissions = db.relationship("RolePermission")
    
    def __repr__(self):
        return self.name
    
    
    def get_permissions_by_mod(self, role_id, mod_id):
        perm = RolePermission.query.filter_by(role_id=role_id, module_id=mod_id).first()
        
        return perm
    
    @staticmethod
    def get_by_id(id):
        return Role.query.get(id)
    

class Module(db.Model, BaseModel):
    
    __tablename__ = "modules"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    
     
    def __repr__(self):
        return self.name 
     
    @staticmethod
    def get_by_id(id):
        return Module.query.get(id)
    
    
class RolePermission(db.Model, BaseModel):
    
    __tablename__ = "role_permissions"
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"))
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id", ondelete="CASCADE"))
    read = db.Column(db.Boolean, default=True)
    write = db.Column(db.Boolean, default=False)
    erase = db.Column(db.Boolean, default=False)
    module = db.relationship("Module")
    
    def __repr__(self):
        return f"Modulo: {self.id}, read:{self.read}, write:{self.write}, delete:{self.erase}" 
     
    def set_permissions(self, read=True, write=False, erase=False):
        print("llada a setpermission")
        self.read = read
        self.write = write
        self.erase = erase
    