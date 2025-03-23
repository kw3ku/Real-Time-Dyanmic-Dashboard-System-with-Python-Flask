from flask import render_template, Blueprint, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, Post

main_routes = Blueprint('main', __name__)
ui_routes = Blueprint('ui', __name__)

@main_routes.route('/')
def index():
    posts = Post.query.order_by(Post.post_id.desc()).all()
    return render_template('index.html', posts=posts)

# Check for database connection
@main_routes.route('/test-db') 
def test_db():
    try:
        # Try to execute a simple query
        db.session.execute("SELECT 1")
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
 

# Render signup form
@main_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        
        if not user_name or not user_email or not user_password:
            flash('All fields are required', 'error')
            return redirect(url_for('main.signup'))
        
        # Check if user already exists
        if User.query.filter_by(user_email=user_email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('main.signup'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
        
        # Create new user
        new_user = User(user_name=user_name, user_email=user_email, user_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.index'))
    
    # Render the signup form for GET requests
    return render_template('signup.html')




# Render login form
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        
        user = User.query.filter_by(user_email=user_email).first()
        if user and bcrypt.check_password_hash(user.user_password, user_password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html')


# endpoints for posts
@main_routes.route('/main.create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        #this is to create the new post 

        new_post = Post(post_title=title, post_content=content, user_id=current_user.user_id)
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    elif request.method == 'GET':
        return render_template('create_post.html')



# Define the dashboard route
@main_routes.route('/dashboard')
@login_required
def dashboard():
    recent_posts = Post.query.filter_by(user_id=current_user.user_id).order_by(Post.post_id.desc()).limit(5).all()
    return render_template('dashboard.html', recent_posts=recent_posts)

# Define the profile route
@main_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# Define the posts route
@main_routes.route('/posts')
@login_required
def posts():
    return render_template('posts.html')

# Define the settings route
@main_routes.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

# Logout route
@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))











# This is more for API purposes 
# CRUD for Users
# @main_routes.route('/users', methods=['POST', 'GET'])
# def users():
#     if request.method == 'POST':
#         data = request.get_json()
#         new_user = User(user_name=data['user_name'], user_email=data['user_email'], user_password=data['user_password'])
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"status": "success", "message": "User created!"})
#     elif request.method == 'GET':
#         users = User.query.all()
#         return jsonify([user.to_dict() for user in users])


# @main_routes.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
# def user(user_id):
#     if request.method == 'GET':
#         user = User.query.get(user_id)
#         return jsonify(user.to_dict())
#     elif request.method == 'PUT':
#         data = request.get_json()
#         user = User.query.get(user_id)
#         user.user_name = data['user_name']
#         user.user_email = data['user_email']
#         user.user_password = data['user_password']
#         db.session.commit()
#         return jsonify({"status": "success", "message": "User updated!"})
#     elif request.method == 'DELETE':
#         user = User.query.get(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({"status": "success", "message": "User deleted!"})

# # CRUD for Posts
# @main_routes.route('/posts', methods=['POST', 'GET'])   
# def posts():
#     if request.method == 'POST':
#         data = request.get_json()
#         new_post = Post(post_title=data['post_title'], post_content=data['post_content'], user_id=data['user_id'])
#         db.session.add(new_post)
#         db.session.commit()
#         return jsonify({"status": "success", "message": "Post created!"})
#     elif request.method == 'GET':
#         posts = Post.query.all()
#         return jsonify([post.to_dict() for post in posts])

