# General imports
from cs50 import SQL
from flask import flash, Flask, redirect, request, render_template, session, url_for
from flask_session import Session
import logging
from werkzeug.security import check_password_hash

# Custom imports
from classes.Client import Client, ClientManager
from classes.Event import Event, EventManager
from classes.Form import FormManager
from classes.Insurance import Insurance, InsuranceManager
from classes.User import User, UserManager
from utils.utils import login_required, redirect_url


# Configure logger
logging.basicConfig(filename='log/report.log', format="%(asctime)s %(message)s", encoding='utf-8',level=logging.DEBUG)

# Configure database using cs50's SQL class
db = SQL("sqlite+pysqlite:///db/register.db", echo=True)

# Initialize the Flask app
app = Flask(__name__)

# Set the SECRET KEY
app.secret_key = "21b0b3b0d2a4111f4f4450d2073ac1ecec66825d2cdc5d1b7e0272acba4a8480"

# Configure the Session class
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Context processor injecting the "admin" variable into all templates 
@app.context_processor
def inject_user_rights():
    """Inform templates whether the user is admin or not"""
    admin = False
    try:
        if session["user_id"]:
            user_manager = UserManager(db)
            admin = True if user_manager.get_details(session["user_id"])["rights"] else False
    except KeyError:
        pass
    finally:
        return dict(admin=admin)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Render contact page"""
    if request.method == "POST":
        contact_details = FormManager.extract_contact_message()
        # TODO: Mail to the company
        flash("Your message was successfully sent. Thank you for getting in touch with us!")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html")
    

@app.route("/")
def index():
   """Render homepage"""
   return render_template("index.html")


@app.route("/insurances")
def insurances():
    """Render offer of insurances"""
    return render_template("insurances.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        email = request.form.get("login_email")
        password = request.form.get("login_password")
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", email
            )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], password
        ):
            flash("Invalid e-mail address or password.")
            return render_template("login.html")
        session["user_id"] = rows[0]["user_id"]
        flash("You have successfully logged in!")
        return redirect(url_for("my_insurances"))
    else:
        return render_template("login.html")
      

@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    session.clear()
    flash("You have been successfully logged out.")
    return render_template("index.html")


@app.route("/my_clients")
@login_required
def my_clients():
    """ADMIN: List all users"""
    client_manager = ClientManager(db)
    clients = client_manager.get_details()
    return render_template("my_clients.html", clients=clients)


@app.route("/my_clients/delete/<int:user_id>", methods=["GET", "POST"])
@login_required
def my_clients_delete(user_id):
    """ADMIN: Delete user from the database"""
    client_manager = ClientManager(db)
    client_manager.delete(user_id)
    flash("You have deleted the user.")
    return redirect(url_for("my_clients"))


@app.route("/my_clients/update/<int:user_id>", methods=["GET", "POST"])
@login_required
def my_clients_update(user_id):
    """ADMIN: Update user's info"""
    client_manager = ClientManager(db)
    if request.method == "POST":
        client_data = FormManager.extract_client()
        client = Client(**client_data, user_id=user_id)
        client_manager.update(client)
        flash("You have successfully updated the client's personal information.")
        return redirect(redirect_url())
    else:
        client = client_manager.get_details(user_id=user_id)
        return render_template("client_detail.html", client=client)


@app.route("/my_details", methods=["GET", "POST"])
@login_required
def my_details():
    """Allow user to change his personal information"""
    client_manager = ClientManager(db)
    if request.method == "POST":
        client_data = FormManager.extract_client()
        client = Client(**client_data, user_id=session["user_id"])
        client_manager.update(client)
        flash("You have successfully updated your personal information.")
        return redirect(redirect_url())
    else:
        client = client_manager.get_details(user_id=session["user_id"])
        return render_template("client_detail.html", client=client)
    

@app.route("/my_insurances/<int:insurance_id>/my_events")
@login_required
def my_events(insurance_id):
    """List user's insurance events for a selected insurance plan"""
    event_manager = EventManager(db)
    events = event_manager.get_all(insurance_id)
    return render_template("my_insurances_events.html", events=events, insurance_id=insurance_id)


@app.route("/my_insurances/<int:insurance_id>/my_events/delete/<int:event_id>", methods=["GET", "POST"])
@login_required
def my_events_delete(insurance_id, event_id):
    """Delete user's insurance event"""
    event_manager = EventManager(db)
    if request.method == "POST":
        event_manager.delete(event_id)
        flash("You have deleted the insurance event.")
        return redirect(url_for("my_events", insurance_id=insurance_id))
    else:
        delete = True
        event = event_manager.get_details(event_id)
        return render_template("event_detail.html", insurance_id=insurance_id, event=event, delete=delete)


@app.route("/my_insurances/<int:insurance_id>/my_events/new", methods=["GET", "POST"])
@login_required
def my_events_new(insurance_id):
    if request.method == "POST":
        """Report a new insurance event"""
        event_manager = EventManager(db)
        form_manager = FormManager(db)
        event_data = form_manager.extract_event()
        new_event = Event(**event_data, insurance_id=insurance_id)
        if event_manager.save(new_event):
            flash("New event was successfully reported.")
        else:
            flash("Invalid file type. Only .docx, .pdf, .jpg, and .png files are allowed.")
        return redirect(url_for('my_events', insurance_id=insurance_id))
    else:
        return render_template("event_detail.html", insurance_id=insurance_id)
    

@app.route("/my_insurances/<int:insurance_id>/my_events/update/<int:event_id>", methods=["GET", "POST"])
@login_required
def my_events_update(insurance_id, event_id):
    """Update user's existing insurance event"""
    event_manager = EventManager(db)
    if request.method == "POST":
        form_manager = FormManager(db)
        event = Event(**form_manager.extract_event(), event_id=event_id)
        if event_manager.update(event):
            flash("You have successfully updated the insurance event.")
        else:
            flash("Invalid file type. Only .docx, .pdf, .jpg, and .png files are allowed.")
        return redirect(url_for('my_events', insurance_id=insurance_id))
    else:
        update = True
        event = event_manager.get_details(event_id)
        return render_template("event_detail.html", insurance_id=insurance_id, event=event, update=update)


@app.route("/my_insurances")
@login_required
def my_insurances():
    """List all active insurances of the user (as an insuree as well as a policyholder)"""
    client_manager = ClientManager(db)
    insurance_manager = InsuranceManager(db)
    client_data = client_manager.get_details(user_id=session["user_id"])
    username = client_manager.get_full_name(client_data["user"])
    insurances = insurance_manager.get_details(client_id=client_data["client_id"], user_rights=client_data["rights"])
    return render_template("my_insurances.html", insurances=insurances, username=username, client=client_data["client_id"])


@app.route("/my_insurances/delete/<int:insurance_id>", methods=["GET", "POST"])
@login_required
def my_insurances_delete(insurance_id):
    """Delete user's existing insurance plan"""
    insurance_manager = InsuranceManager(db)
    if request.method == "POST":
        insurance_manager.delete(insurance_id)
        flash("You have deleted the insurance plan.")
        return redirect(url_for("my_insurances"))
    else:
        delete = True
        client_manager = ClientManager(db)
        username = client_manager.get_full_name(user_id=session["user_id"])
        insurance = insurance_manager.get_details(insurance_id=insurance_id)
        return render_template("my_insurances_detail.html", insurance=insurance, username=username, delete=delete)
    

@app.route("/my_insurances/new", methods=["GET", "POST"])
@login_required
def my_insurances_new():
    """Purchase a new insurance"""
    insurance_manager = InsuranceManager(db)
    form_manager = FormManager(db)
    if request.method == "POST":
        insurance = Insurance(**form_manager.extract_insurance(session["user_id"]))
        if insurance.insuree:
            insurance_manager.save(insurance)
            flash("You have purchased a new insurance plan.")
        else:
            flash("This client is not in our register")
        return redirect(url_for("my_insurances"))
    else:
        client_manager = ClientManager(db)
        insurance_types = Insurance.get_types()
        username = client_manager.get_full_name(session["user_id"])

        # Ensure that the user has filled in their personal information
        if username.strip():
            return render_template("my_insurances_detail.html", username=username, insurance_types=insurance_types)
        flash("You need to fill in your personal information before obtaining a new insurance plan")
        return redirect(url_for("my_details"))


@app.route("/my_insurances/update/<int:insurance_id>", methods=["GET", "POST"])
@login_required
def my_insurances_update(insurance_id):
    """Update user's existing insurance plan"""
    insurance_manager = InsuranceManager(db)
    form_manager = FormManager(db)
    if request.method == "POST":
        insurance = Insurance(**form_manager.extract_insurance(session["user_id"]), insurance_id=insurance_id)
        if insurance.insuree:
            insurance_manager.update(insurance)
            flash("You have updated the insurance plan.")
        else:
            flash("This client is not in our register")
        return redirect(url_for("my_insurances"))
    else:
        update = True
        client_manager = ClientManager(db)
        insurance_types = Insurance.get_types()
        username = client_manager.get_full_name(session["user_id"])
        insurance = insurance_manager.get_details(insurance_id=insurance_id)
        return render_template("my_insurances_detail.html", insurance=insurance, username=username, update=update, insurance_types=insurance_types)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register a new user (step one)"""
    if request.method == "POST":
        user_data = FormManager.extract_user()

        # Check password confirmation before proceeding
        if user_data["password"] != user_data["password_conf"]:
            flash("The passwords are not identical.")
            return render_template("signup.html")

        new_user = User(user_data["email"], user_data["password"])
        
        # Collect all error messages and flash them, if any
        errors = []
        if not new_user.is_email_valid():
            errors.append("Invalid email address.")
        if not new_user.is_password_valid():
            errors.append("Your password is too short (enter at least 8 characters).")
        if errors:
            for error in errors:
                flash(error)
            return render_template("signup.html")

        user_manager = UserManager(db)

        # Save the user if all checks pass
        try:
            user_manager.save(new_user)
            flash("You have been successfully signed up. Please continue with step 2.")
            return render_template("client_detail.html")
        except ValueError:
            flash("This e-mail address is already in our database. Please log in.")

    return render_template("signup.html")


@app.route("/signup_client", methods=["GET", "POST"])
def signup_client():
    """Get more information about the user and save them as "client" (step 2)"""
    if request.method == "POST":
        # Extract form data
        client_data = FormManager.extract_client()
        user_id = session.get("user_id") or db.execute("SELECT MAX(user_id) FROM users")[0]["MAX(user_id)"]

        # Create a Client object with the form data
        client = Client(user_id=user_id, **client_data)

        # Use ClientManager to insert or update the client
        client_manager = ClientManager(db)
        if client_manager.exists(client.user_id):
            client_manager.update(client)
            flash("Your details have been successfully updated.")
            return redirect(redirect_url())
        else:
            client_manager.save(client)
            flash("You have successfully signed up. Please, log in.")
            return redirect(url_for("login"))

    else:
        return render_template("client_detail.html")


@app.route("/testimonials")
def testimonials():
    """Render testimonials page"""
    return render_template("testimonials.html")


if __name__ == "__main__":
   app.run(debug=True)