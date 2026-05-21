from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Database Path Parameter Definition
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaspera.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- FINALIZE DATABASE MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    quiz_answers = db.Column(db.String(255), default="")
    has_paid_fee = db.Column(db.Boolean, default=False)

# --- BACKEND REGISTRATION LOGIC ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register_user():
    """
    Captures form data and generates a unique user row inside the database.
    """
    data = request.get_json()
    username_input = data.get('username')
    email_input = data.get('email')
    
    if not username_input or not email_input:
        return jsonify({"error": "Missing critical parameters"}), 400
        
    # Safety Check: Verify username uniqueness parameter
    if User.query.filter_by(username=username_input).first():
        return jsonify({"error": "Identity handle already registered"}), 400
        
    new_user = User(username=username_input, email=email_input)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "Identity registered into ecosystem",
        "user_id": new_user.id
    })

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """
    Binds the calculated questionnaire matrix string directly to the active user profile.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    vector_string = data.get('answers')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User target verification failed"}), 404
        
    user.quiz_answers = vector_string
    db.session.commit()
    return jsonify({"success": True, "message": "Worldview synchronization saved"})

# --- PWA CONNECTIVITY CONFIGURATIONS ---

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def serve_sw():
    response = app.make_response(app.send_static_file('sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensures your system automatically writes the new User columns
    app.run(debug=True, port=5000)
        
