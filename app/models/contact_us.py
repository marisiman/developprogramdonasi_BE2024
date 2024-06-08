from app.utils.db import db
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import bcrypt

class Contact_us(db.Model):
    __tablename__ = "contact_us"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    user = db.relationship('User', backref='contacts')

    def __repr__(self):
        return f"ContactUs('{self.first_name}', '{self.last_name}', '{self.email}')"
    
    def serialize(self, full=True):
        if full:
            data = {
                'id': self.id,
                'user_id' : self.user_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'message': self.message
            }
            if self.created_at:
                data['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            return data
        else:
            return {
                'id': self.id,
                'user_id' : self.user_id,
                'first_name': self.first_name,
                'email': self.email,
                'message': self.message
            }
