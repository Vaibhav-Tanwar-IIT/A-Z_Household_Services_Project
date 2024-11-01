from flask_sqlalchemy import SQLAlchemy
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
    email = db.Column(db.String(120), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    service_name = db.Column(db.String(100), nullable=False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_name = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)

class Login(db.Model):
    __tablename__ = "login"
    email = db.Column(db.Text, primary_key=True)
    password = db.Column(db.String(10))
    def __init__(self, email, password):
        self.email = email
        self.password = password