import json
import logging

from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .models import db, Student, Staff
from .infobot import infobot_bp, routes as infobot_routes
from .DocBot import docbot_bp


# 1. Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('infobot@123')

def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)
    app.secret_key = os.urandom(24)  # Random secret key

    # 2. Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 3. Load FAQs and scrape site on startup
    with app.app_context():
        infobot_routes.scrape_and_structure_website_selenium(infobot_routes.BASE_URL)

    # 4. Register Blueprints
    app.register_blueprint(infobot_bp, url_prefix='/infobot')
    app.register_blueprint(docbot_bp, url_prefix='/docbot')


    # 5. Define Routes
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/docbot')
    def docbot():
        return render_template('docbot.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user_type = request.form['user_type']
            name = request.form['name']
            email = request.form['email']

            if user_type == 'student':
                usn = request.form['usn']
                batch = request.form['batch']
                branch = request.form['branch']
                pass_out_year = request.form['pass_out_year']

                existing_student = Student.query.filter((Student.email == email) | (Student.usn == usn)).first()
                if existing_student:
                    flash("Email or USN already registered!", "danger")
                    return redirect(url_for('register'))

                new_student = Student(name=name, batch=batch, usn=usn, email=email, branch=branch, pass_out_year=pass_out_year)
                db.session.add(new_student)

            elif user_type == 'staff':
                unique_id = request.form['unique_id']
                existing_staff = Staff.query.filter((Staff.email == email) | (Staff.unique_id == unique_id)).first()
                if existing_staff:
                    flash("Email or Unique ID already registered!", "danger")
                    return redirect(url_for('register'))

                new_staff = Staff(name=name, unique_id=unique_id, email=email)
                db.session.add(new_staff)

            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            usn = request.form['usn']

            student = Student.query.filter_by(email=email, usn=usn).first()
            if student:
                session['user'] = email
                session['user_type'] = 'student'
                flash("Login Successful!", "success")
                return redirect(url_for('staff_chat'))

            staff = Staff.query.filter_by(email=email, unique_id=usn).first()
            if staff:
                session['user'] = email
                session['user_type'] = 'staff'
                flash("Login Successful!", "success")
                return redirect(url_for('staff_chat'))

            flash("Invalid credentials!", "danger")

        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user' not in session:
            flash("Please login first!", "warning")
            return redirect(url_for('login'))

        return redirect(url_for('staff_chat'))

    @app.route('/visitor-chat')
    def visitor_chat():
        return render_template('visitor_chat.html')

    @app.route('/staff-chat')
    def staff_chat():
        return render_template('staff_chat.html')

    @app.route("/submit", methods=["POST"])
    def submit():
        infrastructure = request.form.get("infrastructure", "No response")
        challenges = request.form.get("challenges", "No response")
        infobot = request.form.get("infobot", "No response")
        suggestion = request.form.get("suggestion", "No response")

        submission = f"""
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Infrastructure Rating: {infrastructure}
Communication Challenges: {challenges}
InfoBot Feedback: {infobot}
Suggestions: {suggestion}
-------------------------------
"""

        file_path = os.path.join(os.getcwd(), "submissions.txt")

        try:
            with open(file_path, "a") as file:
                file.write(submission)

            app.logger.info("Submission saved successfully")
            return "<h3 style='color: green;'>Submission saved successfully!</h3>", 200
        except Exception as e:
            app.logger.error(f"Error saving submission: {e}")
            return "<h3 style='color: red;'>An error occurred while saving your submission.</h3>", 500

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('user_type', None)
        flash("Logged out successfully!", "info")
        return redirect(url_for('login'))

    @app.route('/about')
    def about():
        return render_template('about.html')

    ### Admin Login Routes
    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
                session['admin_logged_in'] = True
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('admin_login'))

        return render_template('admin_login.html')

    @app.route('/admin_dashboard')
    def admin_dashboard():
        if not session.get('admin_logged_in'):
            flash('Please login as admin first.', 'warning')
            return redirect(url_for('admin_login'))
        return render_template('admin_dashboard.html')

    @app.route('/admin_logout')
    def admin_logout():
        # Clear the session data
        session.pop('admin_logged_in', None)

        # Flash a message confirming the admin logged out
        flash('Admin logged out successfully!', 'info')

        # Redirect to the admin login page
        return redirect(url_for('admin_login'))

    @app.route('/submissions')
    def submissions():
        submissions_file = os.path.join(app.root_path, '..', 'submissions.txt')  # Adjust path if needed
        try:
            with open(submissions_file, 'r') as file:
                submissions_content = file.read()
        except FileNotFoundError:
            submissions_content = "No submissions found."

        return render_template('submissions.html', submissions=submissions_content)

    return app

