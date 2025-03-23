from flask import render_template, Blueprint, request, redirect, url_for
from . import db
from .models import User


main_routes = Blueprint('main_routes', __name__)

# Render signup form
@main_routes.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# signup form for backend 
@main_routes.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not name or not email or not password:
        return "All fields are required", 400
    
    # Hash the password (use a library like Flask-Bcrypt)
    hashed_password = password  # Replace with actual hashing
    
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.dashboard'))


# Render login form
@main_routes.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


# Render create post form
@main_routes.route('/create-post', methods=['GET'])
def create_post_form():
    return render_template('create_post.html')