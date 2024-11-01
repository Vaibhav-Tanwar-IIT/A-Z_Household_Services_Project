from flask import Flask, render_template, request, redirect, url_for, flash, session
from model.model import Service, ServiceRequest, Professional, Login,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_database.db'
app.config['SECRET_KEY'] = 'my_very_very_super_duper_extremely_long_secret_key'
db.init_app(app)
users = dict()

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        # User Login
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(Login).filter_by(email=email).first()

        if user is not None and user.password == password:
            return redirect(url_for("customer_dashboard"))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html')


# Route for the Admin Dashboard
@app.route('/admin_dashboard', methods=["GET", "POST"])
def admin_dashboard():
    services = Service.query.all()
    professionals = Professional.query.all()
    service_requests = ServiceRequest.query.all()
    return render_template('admin_dashboard.html', services=services, professionals=professionals, service_requests=service_requests)

# Route to Add a New Service
@app.route('/add_new_service', methods=['POST'])
def add_new_service():
    service_name = request.form.get('service_name')
    description = request.form.get('description')
    base_price = request.form.get('base_price')

    if not service_name or not description or not base_price:
        flash("All fields are required!", "danger")
        return redirect(url_for('admin_dashboard'))

    new_service = Service(service_name=service_name, description=description, base_price=base_price)
    db.session.add(new_service)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

# Route for Admin Search Functionality
@app.route('/admin_search', methods=['GET'])
def admin_search():
    search_by = request.args.get('search_by')
    search_text = request.args.get('search_text')
    
    if search_by == 'service':
        results = Service.query.filter(Service.service_name.ilike(f'%{search_text}%')).all()
    elif search_by == 'customer':
        results = ServiceRequest.query.filter(ServiceRequest.customer_name.ilike(f'%{search_text}%')).all()
    elif search_by == 'professional':
        results = Professional.query.filter(Professional.email.ilike(f'%{search_text}%')).all()
    else:
        results = []
    
    return render_template('admin_search_results.html', results=results, search_by=search_by, search_text=search_text)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        return redirect(url_for("admin_dashboard"))
    return render_template('admin_login.html')

@app.route('/customer_signup', methods=["GET", "POST"])
def customer_signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Login(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('customer_signup.html')

@app.route('/professional_register', methods=["GET", "POST"])
def professional_register():
    if request.method == "POST":
        return redirect(url_for('professional_dashboard'))
    return render_template('professional_registration.html')

@app.route('/professional_dashboard')
def professional_dashboard():
    # Sample data for the dashboard
    today_services = [
        {"customer_name": "John Doe", "contact_phone": "123-456-7890", "location": "New York, 10001"},
        {"customer_name": "Alice Smith", "contact_phone": "987-654-3210", "location": "San Francisco, 94101"}
    ]
    closed_services = [
        {"customer_name": "Jane Smith", "contact_phone": "987-654-3210", "location": "Los Angeles, 90001", "date": "2024-10-31", "rating": 4.5},
        {"customer_name": "Mark Johnson", "contact_phone": "555-234-5678", "location": "Chicago, 60601", "date": "2024-09-21", "rating": 3.8}
    ]
    # Data for the charts
    reviews_data = [45, 25, 20, 10]  # Dummy data for pie chart
    requests_data = [50, 30, 20]     # Dummy data for bar chart

    return render_template('professional_dashboard.html', 
                           today_services=today_services, 
                           closed_services=closed_services,
                           reviews_data=reviews_data,
                           requests_data=requests_data)

@app.route('/customer_dashboard')
def customer_dashboard():
    # Sample data for different sections in the dashboard
    service_options = ["AC Repair", "Salon", "Cleaning", "Electrician"]
    
    service_history = [
        {"id": 1, "service_name": "Cleaning", "professional_name": "Alice Smith", "phone": "123-456-7890", "status": "Closed"},
        {"id": 2, "service_name": "Salon", "professional_name": "Bob Johnson", "phone": "987-654-3210", "status": "Requested"}
    ]
    
    salon_packages = [
        {"id": 1, "name": "Full Salon Package", "details": "Includes hair styling, manicure, etc.", "price": "$100"},
        {"id": 2, "name": "Basic Salon Package", "details": "Includes hair wash, blow dry, etc.", "price": "$50"}
    ]
    
    # Data for ChartJS
    request_stats = [30, 15, 5]  # Example data: Requested, Closed, Assigned

    return render_template('customer_dashboard.html', 
                           service_options=service_options, 
                           service_history=service_history,
                           salon_packages=salon_packages,
                           request_stats=request_stats)

@app.route("/submit_remark", methods=["POST"])
def submit_remark():
    return redirect(url_for("customer_dashboard"))

@app.route('/delete_service/<int:service_id>', methods=["POST"])
def delete_service(service_id):
    service = Service.query.get(service_id)
    
    if service:
        # Delete the service if it exists
        db.session.delete(service)
        db.session.commit()

    # Redirect back to the admin dashboard
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/customer_ratings')
def customer_ratings():
    # Example data
    ratings = {
        '5_star': 30,
        '4_star': 20,
        '3_star': 15,
        '2_star': 10,
        '1_star': 5
    }
    return ratings

@app.route('/api/service_requests_summary')
def service_requests_summary():
    summary = {
        'requested': 50,
        'accepted': 35,
        'closed': 20
    }
    return summary

if __name__ == '__main__':
    app.run(debug=True)
