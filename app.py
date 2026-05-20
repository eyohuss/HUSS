from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Configuration for SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaspera.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev_secret_key_12345'

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    has_paid = db.Column(db.Boolean, default=False)
    payment_tier = db.Column(db.Integer, default=0) # e.g., 30 or 50 Euros
    
    # Relationships
    answers = db.relationship('Answer', backref='user', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., "Lifestyle", "Values"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False) # Values 1 to 5 (Scale options)

# Database Initialization Helper
def seed_initial_data():
    if Question.query.count() == 0:
        sample_questions = [
            Question(text="How important is personal runtime flexibility over planned schedules?", category="Lifestyle"),
            Question(text="Do you prefer deep abstract concepts over practical immediate solutions?", category="Intellect"),
            Question(text="How highly do you value quiet isolation vs social gatherings?", category="Social"),
            Question(text="Is financial transparency critical from day one of a relationship?", category="Values")
        ]
        db.session.bulk_save_objects(sample_questions)
        db.session.commit()

# Application Routing Definitions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Username already configured"}), 400
        
    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        has_paid=False
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Account initialized", "user_id": new_user.id})

@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    user = User.query.get(data.get('user_id'))
    tier_fee = int(data.get('fee', 30)) # Expects 30 to 50 Euro value
    
    if user:
        user.has_paid = True
        user.payment_tier = tier_fee
        db.session.commit()
        return jsonify({"message": f"Payment of €{tier_fee} verified successfully", "access": True})
    return jsonify({"error": "User validation failure"}), 404

@app.route('/api/questions', methods=['GET'])
def get_questions():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    
    if not user or not user.has_paid:
        return jsonify({"error": "Access Denied: Payment verified entry required"}), 403
        
    questions = Question.query.all()
    output = [{"id": q.id, "text": q.text, "category": q.category} for q in questions]
    return jsonify({"questions": output})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial_data()
    app.run(debug=True)

