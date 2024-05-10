from urllib.parse import urlsplit
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # print('enter validate')
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None:
            register_link = '<a href="{}">register</a>'.format(url_for('register'))
            flash('User not found. Please {} first.'.format(register_link), 'info')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))

        login_user(user)

        return redirect(url_for('gallery'))
    return render_template('login.html', title="Log In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form here
        # Validate form data, create user, etc.
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/manage-account', methods=['GET', 'POST'])
@login_required
def manage_account():
    if request.method == 'POST':
        # Process changes here
        return redirect(url_for('account'))
    return render_template('manage-account.html')

@app.route('/item')
@login_required
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