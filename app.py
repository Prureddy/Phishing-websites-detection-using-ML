from flask import *
from flask import render_template, redirect, url_for, session, flash
#from werkzeug.utils import secure_filename
import os  
from test import main
from train import training
from functools import wraps
import secrets

app = Flask(__name__)  
app.secret_key = secrets.token_hex(16)  # Generate a random secret key

# Predefined users (in a real app, you'd use a database with hashed passwords)
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
    "user2": {"password": "pass456", "role": "user"}
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')  
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("topic.html", username=session.get('username'))

@app.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    # Only allow admins to train the model
    if session.get('role') != 'admin':
        flash('You do not have permission to train the model', 'danger')
        return redirect(url_for('dashboard'))
    
    training()
    flash('Model training completed successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if request.method == 'POST':
        text = request.form['text'] 
        outfile = open("data.txt", "w")
        outfile.write(text)
        outfile.close()
    
    prediction = main()
    if prediction == -1:
        my_variable = "you got a phishing website"
    else:
        my_variable = "safe"
    
    return render_template("success.html", my_variable=my_variable, username=session.get('username'))

@app.route('/success', methods=['POST'])  
@login_required
def success():  
    if request.method == 'POST':
        text = request.form['text'] 
        outfile = open("data.txt", "w")
        outfile.write(text)
        outfile.close()
        return render_template("success.html", username=session.get('username'))

if __name__ == '__main__':  
    app.run(debug=True)