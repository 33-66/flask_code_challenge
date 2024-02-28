# from wsgiref.validate import validator
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import Enum

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    super_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    powers = db.relationship("Hero_power", backref="Hero_power")


class Power(db.Model): 
    __tablename__ = "powers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    
    @validates("description")
    def validate_description(self, description, key):
        if len(description) < 20:
            raise ValueError("Must be more than 20 characters long")
        else:
            return description


class Hero_power(db.Model):
    __tablename__ = "hero_powers"
    id = db.Column(db.Integer, primary_key=True)
    strength = Enum('Strong', 'Weak', 'Average')
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    
    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')
