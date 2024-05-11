from app import app, db
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

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/admin/index')
@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/manage-items', methods=['GET']) 
def admin_manage_items(): 
    return render_template('admin/manage-items.html')

@app.route('/admin/new-item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        # Process new item form here
        return redirect(url_for('admin_manage_item'))
    return render_template('admin/new-item.html')