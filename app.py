from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaspera.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Core User Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    has_paid_fee = db.Column(db.Boolean, default=False) 

# Main Web Screen Route
@app.route('/')
def index():
    return render_template('index.html')

# Mobile Download Connection Configuration
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
                                
