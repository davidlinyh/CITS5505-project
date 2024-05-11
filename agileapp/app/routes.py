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
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))  # Redirect to a useful page post-login

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None:
            flash('User not found. Please register first.', 'info')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data if 'remember_me' in form else False)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('gallery'))  # Redirect to `next` page or `gallery`

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print('enter register')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("enter validation")
        user = User(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Success! Please Log in to continue.')
        return redirect(url_for('login'))
    print(form.data)
    print(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/manage-account', methods=['GET', 'POST'])
@login_required
def manage_account():
    if request.method == 'POST':
        # Process changes here
        return redirect(url_for('account'))
    return render_template('manage-account.html', user=current_user)

@app.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = LostItem.query.get_or_404(item_id)  # Fetch the item or return 404 if not found
    return render_template('item.html', item=item)

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