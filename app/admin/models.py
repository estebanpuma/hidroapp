from flask_login import UserMixin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from app import db 


class BaseModel():
    def save(self, db_session=db.session):
        try:
            if not self.id:
                db_session.add(self)
                db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error occurred while saving: {e}")

    def delete(self, db_session=db.session):
        try:
            if self.id:
                db_session.delete(self)
                db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error occurred while deleting: {e}")
            
class User(db.Model, UserMixin, BaseModel):
    
    __tablename__ = "app_users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    birth = db.Column(db.Date)
    
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
    
 # Creación de un usuario por defecto
