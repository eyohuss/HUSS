from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaspera.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Storing answers as a simple comma-separated string string parameter (e.g., "5,3,4,1")
    quiz_answers = db.Column(db.String(255), default="")

# --- COMPATIBILITY ENGINE LOGIC ---

def calculate_alignment(user_answers, candidate_answers):
    """
    Calculates compatibility using a distance formula variable.
    Returns a percentage matching parameter from 0% to 100%.
    """
    # Convert string storage paths back into arrays of integers
    u_list = [int(x) for x in user_answers.split(',') if x]
    c_list = [int(x) for x in candidate_answers.split(',') if x]
    
    if len(u_list) != len(c_list) or len(u_list) == 0:
        return 0 # Fallback check for missing profile data
        
    # Calculate the sum of squared differences
    squared_diffs = sum((u - c) ** 2 for u, c in zip(u_list, c_list))
    max_possible_distance = len(u_list) * (4 ** 2) # Max variation between a 1 and 5 answer
    
    # Invert the mathematical difference parameter into a clean percentage match
    alignment_score = 100 * (1 - (squared_diffs / max_possible_distance))
    return round(alignment_score, 1)

# --- APPLICATION ROUTING ENDPOINTS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['GET'])
def find_matches():
    current_user_id = request.args.get('user_id')
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.quiz_answers:
        return jsonify({"error": "Profile vectors incomplete"}), 400
        
    all_candidates = User.query.filter(User.id != current_user.id).all()
    curated_matches = []
    
    for candidate in all_candidates:
        if candidate.quiz_answers:
            # Run the matching algorithm parameters across profiles
            score = calculate_alignment(current_user.quiz_answers, candidate.quiz_answers)
            
            # Elite European threshold: Only include connections with a high affinity parameter
            if score >= 75.0:
                curated_matches.append({
                    "username": candidate.username,
                    "alignment": f"{score}%"
                })
                
    # Sort matches so the closest geometric trajectories appear first
    curated_matches = sorted(curated_matches, key=lambda x: x['alignment'], reverse=True)
    return jsonify({"curated_refinement": curated_matches})

# --- PWA SERVER SYSTEM ENDPOINTS ---

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
        db.create_all()
    app.run(debug=True, port=5000)
        
