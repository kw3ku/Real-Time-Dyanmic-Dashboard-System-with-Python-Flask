# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
# db = SQLAlchemy(app)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# # from sqlalchemy import exc
# from config import Config

# # Initialize SQLAlchemy
# db = SQLAlchemy()

# def create_app():
#     # Create the Flask app
#     app = Flask(__name__)
    
#     # Load configuration
#     app.config.from_object(Config)
    
#     # Initialize SQLAlchemy with the app
#     db.init_app(app)
    
#     # Test MySQL connection
#     with app.app_context():
#         try:
#             # Try to establish a connection
#             db.engine.connect()
#             print("✅ Successfully connected to MySQL!")
#         except exc.SQLAlchemyError as e:
#             print("❌ Failed to connect to MySQL:", str(e))
#             raise  # Stop the app if the connection fails
    
#     return app


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text  # Import the text function

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Route to test database connection
@app.route('/test-db')
def test_db():
    try:
        # Try to execute a simple query
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)