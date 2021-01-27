import uuid
import os

from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_session, init_db
from models import User, Post, Topic
from login import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CVEdiffiehelman'
login_manager.init_app(app)
init_db()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 400

@app.errorhandler(500)
def internal_error(e):
	return render_template("error_500.html"), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        secure_password = generate_password_hash(password)
        confirm_pasword = request.form['verify_password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash("This username already exists!","danger")
            return render_template("register.html")
        if confirm_pasword == password:
            user = User(username=username, password=secure_password)
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('index'))
        else:
            flash("Passwords doesn`t match!","danger")
    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    current_user.login_id = None
    db_session.commit()
    logout_user()
    return redirect(url_for('login'))