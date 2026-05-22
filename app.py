from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_fallback_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaspera.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    quiz_answers = db.Column(db.String(255), default="")

# --- MANDATORY PRODUCTION DATABASE INITIALIZATION ---
# This executes unconditionally on boot, regardless of Gunicorn server structures.
with app.app_context():
    db.create_all()

# --- INTERACTIVE ACCOUNT REGISTRATION API ---
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid request payload format"}), 400
            
        username_input = data.get('username', '').strip()
        email_input = data.get('email', '').strip()
        
        if not username_input or not email_input:
            return jsonify({"status": "error", "message": "Identity fields cannot remain empty"}), 400
            
        new_user = User(username=username_input, email=email_input)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"status": "success", "user_id": new_user.id}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "This unique handle or email is already registered"}), 409
        
    except Exception as general_error:
        db.session.rollback()
        return jsonify({"status": "error", "message": "An unexpected synchronization anomaly occurred"}), 500

# --- INTERACTIVE QUIZ METRIC SUBMISSION API ---
@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        vector_string = data.get('answers')
        
        if not user_id or not vector_string:
            return jsonify({"status": "error", "message": "Missing matrix routing telemetry"}), 400
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "Profile identity search returned negative"}), 404
            
        user.quiz_answers = vector_string
        db.session.commit()
        return jsonify({"status": "success", "message": "Worldview synchronization saved"})
        
    except Exception as general_error:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Matrix writing failure intercepted"}), 500

# --- CORE FRONTEND ENTRY ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def serve_sw():
    response = app.make_response(app.send_static_file('sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
