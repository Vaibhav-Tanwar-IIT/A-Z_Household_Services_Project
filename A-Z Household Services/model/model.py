from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Float, nullable=False)

    def __init__(self, service_name, description, base_price):
        self.service_name = service_name
        self.description = description
        self.base_price = base_price

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    def __init__(self, name, email, password, experience, service_name, phone):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password
        self.experience = experience
        self.service_name = service_name
        self.phone = phone

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_name = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    def __init__(self, professional_name, customer_name, status) -> None:
        super().__init__()
        self.professional_name = professional_name
        self.customer_name = customer_name
        self.status = status

class ServiceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(20), nullable=False)
    professional_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    def __init__(self, service_name, professional_name, email, state='requested') -> None:
        super().__init__()
        self.service_name = service_name
        self.professional_name = professional_name
        self.email = email
        self.state = state

class TodayService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    service_requested = db.Column(db.String(80), nullable=False)
    def __init__(self, customer_name, contact, location, service_requested) -> None:
        super().__init__()
        self.customer_name = customer_name
        self.contact = contact
        self.location = location
        self.service_requested = service_requested

class ClosedService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(6), nullable=False, default="-/-")
    date = db.Column(db.DateTime, default=datetime.now())
    def __init__(self, customer_name, contact, location, rating) -> None:
        super().__init__()
        self.customer_name = customer_name
        self.contact = contact
        self.location = location
        self.rating = rating

class CustomerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10))
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(8), nullable=False)
    def __init__(self, email, password, name, phone, address, postal_code) -> None:
        super().__init__()
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address
        self.postal_code = postal_code