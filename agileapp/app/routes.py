from app import app
from flask import render_template, request, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login code here
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form here
        # Validate form data, create user, etc.
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/manage-account', methods=['GET', 'POST'])
def manage_account():
    if request.method == 'POST':
        # Process changes here
        return redirect(url_for('account'))
    return render_template('manage-account.html')