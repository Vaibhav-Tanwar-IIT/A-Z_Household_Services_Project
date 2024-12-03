from flask import Flask, render_template, request, redirect, url_for, flash, session
from model.model import Service, ServiceRequest, Professional, ServiceHistory, CustomerData, TodayService, ClosedService, db
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_database.db'
app.config['SECRET_KEY'] = 'my_very_very_super_duper_extremely_long_secret_key'
app.secret_key = "some_random_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)
users = dict()
session

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # User Login
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(CustomerData).filter_by(email=email).first()

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

@app.route("/reject_professional/<int:professional_id>", methods=["GET"])
def reject_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if professional:
        db.session.delete(professional)
        db.session.commit()

    return redirect(url_for('admin_dashboard'))

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
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        postal_code = request.form.get("postal_code")
        session["user_name"] = name
        session["user_contact"] = phone
        user_data = CustomerData(email=email, password=password, name=name, 
                                 phone=phone, address=address, postal_code=postal_code)
        db.session.add(user_data)
        db.session.commit()
        print(session)
        return redirect(url_for('login'))
    
    return render_template('customer_signup.html')

@app.route('/professional_register', methods=["GET", "POST"])
def professional_register():
    available = Service.query.filter_by(service_name=Service.service_name).all()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("fullname")
        experience = request.form.get("experience")
        phone = request.form.get("phone")
        service_name = request.form.get("service_name")

        professional = Professional(email=email, password=password, name=name, 
                                    experience=experience, service_name=service_name, phone=phone)

        db.session.add(professional)
        db.session.commit()
    
        return redirect(url_for('professional_dashboard'))
    return render_template('professional_registration.html', available=available)

@app.route('/professional_dashboard')
def professional_dashboard():
    # Sample data for the dashboard
    services = TodayService.query.all()
    today_services = []
    for s in services:
        d = {}
        d['id'] = s.id
        d["customer_name"] = s.customer_name
        d["contact_phone"] = s.contact
        d["location"] = s.location
        d["service_name"] = s.service_requested

        today_services.append(d)

    c_services = ClosedService.query.all()
    closed_services = []
    for service in c_services:
        serve = {}
        serve["customer_name"] = service.customer_name
        serve["contact_phone"] = service.contact
        serve["location"] = service.location
        serve["date"] = service.date
        serve["rating"] = service.rating

        closed_services.append(serve)

    print(today_services)
    print(services)
    # Data for the charts
    reviews_data = [45, 25, 20, 10]  # Dummy data for pie chart
    requests_data = [50, 30, 20]     # Dummy data for bar chart

    print(session)
    return render_template('professional_dashboard.html', 
                           today_services=today_services, 
                           closed_services=closed_services,
                           reviews_data=reviews_data,
                           requests_data=requests_data)

@app.route("/professional/accept_service/<service_name>")
def accept_service(service_name):
    service = ServiceHistory.query.filter_by(service_name=service_name).all()
    for i in service:
        i.state = "accepted"
        # db.session.add(s)
    service_hist = ServiceHistory.query.filter_by(service_name=service_name).first()
    professional_name = service_hist.professional_name
    services = TodayService.query.filter_by(service_requested=service_name).first()
    service_req = ServiceRequest(customer_name=services.customer_name, status="A", professional_name=professional_name)
    db.session.add(service_req)
    db.session.delete(services)
    print(services)
    db.session.commit()
    return redirect(url_for("professional_dashboard"))

@app.route("/professional/reject_service/<int:service_id>")
def reject_service(service_id):
    rejected_services = TodayService.query.get(service_id)
    service_hist = ServiceHistory.query.filter_by(service_name=rejected_services.service_requested).first()
    professional_name = service_hist.professional_name
    service_req = ServiceRequest(customer_name=rejected_services.customer_name, status="R", professional_name=professional_name)
    db.session.add(service_req)
    db.session.delete(rejected_services)
    db.session.delete(service_req)
    db.session.commit()
    return redirect(url_for("professional_dashboard"))
@app.route('/customer_dashboard')
def customer_dashboard():
    print(len(session))
    # Sample data for different sections in the dashboard
    service_options = Service.query.filter_by(service_name=Service.service_name).all()
    packages = Service.query.all()
    selected = []
    for i in packages:
        d = {}
        d['id'] = i.id
        d['name'] = i.service_name
        d['details'] = i.description
        d['price'] = i.base_price
        selected.append(d)

    services = ServiceHistory.query.all()
    print(services)
    service_history = []
    for s in services:
        print(s.service_name)
        d = {}
        d["service_name"] = s.service_name
        d["professional_name"] = s.professional_name
        d["email"] = s.email

        service_history.append(s)
    # Data for ChartJS
    request_stats = [30, 15, 5]  # Example data: Requested, Closed, Assigned

    return render_template('customer_dashboard.html', 
                           service_options=service_options, 
                           service_history=service_history,
                           salon_packages=selected,
                           request_stats=request_stats)

@app.route('/customer/book_service/<int:service_id>', methods=['GET'])
def book_service(service_id):
    service = Service.query.get(service_id)
    s_name = service.service_name
    professional = Professional.query.filter_by(service_name=service.service_name).first()
    professional_name = professional.name
    email = professional.email
    service_history = ServiceHistory(service_name=s_name, professional_name=professional_name,
                                     email=email)
    customer_no = session.get("user_contact")
    customer_name = session.get("user_name")
    user = CustomerData.query.filter_by(phone=customer_no).first()
    address = user.address
    ordered_service = TodayService(customer_name=customer_name, contact=customer_no, location=address, service_requested=s_name)
    print(session.items())
    db.session.add(service_history)
    db.session.add(ordered_service)
    db.session.commit()

    return redirect(url_for("customer_dashboard"))

@app.route("/submit_remark", methods=["POST"])
def submit_remark():
    service_id = request.form.get("service_id")
    service_name = request.form.get("service_name")
    rating = request.form.get("rating")
    customer = CustomerData.query.filter_by(phone=session.get("user_contact")).first()
    location = customer.address
    user_name = customer.name
    contact = customer.phone
    # phone_no = CustomerData.query.filter_by(phone=CustomerData.phone).first()
    closed_service = ClosedService(customer_name=user_name, contact=contact, location=location, rating=rating)
    service = ServiceHistory.query.get(service_id)
    db.session.add(closed_service)
    db.session.delete(service)
    db.session.commit()
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
