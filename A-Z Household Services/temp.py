from model.model import CustomerData, db
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_database.db'
app.config['SECRET_KEY'] = 'my_very_very_super_duper_extremely_long_secret_key'
db.init_app(app=app)
with app.app_context():
    phone_no = CustomerData.query.filter_by(phone=CustomerData.phone).all()
    for i in phone_no:
        print(i.phone)

if __name__ == "__main__":
    app.run(debug=True)