from urllib.parse import urlsplit
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, LostItem, Claim

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
    items = LostItem.query.all() # Fetch all lost items from the database
    return render_template('gallery.html', items=items)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/manage-account', methods=['GET', 'POST'])
@app.route('/manage-account', methods=['GET', 'POST'])
@login_required
def manage_account():
    if request.method == 'POST':
        # Process form data and update user information
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']

        # Handle profile picture update
        

        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    return render_template('manage-account.html', user=current_user)

@app.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = LostItem.query.get_or_404(item_id)  # Fetch the item or return 404 if not found
    return render_template('item.html', item=item)

@app.route('/admin/index')
@app.route('/admin')
@login_required
def admin_index():
    recent_items = LostItem.query.order_by(LostItem.updated_at.desc()).limit(5).all()
    recent_claims = Claim.query.order_by(Claim.updated_at.desc()).limit(5).all()
    return render_template('admin/index.html', recent_items=recent_items, recent_claims=recent_claims)

@app.route('/admin/manage-items', methods=['GET']) 
def admin_manage_items(): 
    items = LostItem.query.all() # Fetch all lost items from the database
    return render_template('admin/manage-items.html', items=items)

@app.route('/admin/new-item', methods=['GET', 'POST'])
@login_required
def new_item():
    if request.method == 'POST':
        try:
            new_item = LostItem(
                name=request.form['name'],
                description=request.form['description'],
                tags=request.form['location'],  # Assuming 'location' is stored as 'tags'
                photo_paths=request.files['image'].filename,  # This assumes you handle file saving separately
                status='Available',  # Default status
                admin_id=current_user.id  # Assuming the admin's user ID is needed
            )
            db.session.add(new_item)
            db.session.commit()
            flash('New item added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding item: {}'.format(e), 'error')
        return redirect(url_for('admin_manage_items'))
    return render_template('admin/new-item.html')

@app.route('/admin/edit-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_item(item_id):
    item = db.session.query(LostItem).filter_by(id=item_id).first()
    if request.method == 'POST':
        if item:
            item.name = request.form.get('name', item.name)
            item.description = request.form.get('description', item.description)
            item.tags = request.form.get('tags', item.tags)
            item.photo_paths = request.form.get('photo_paths', item.photo_paths)
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('admin_manage_items'))
        else:
            flash('Item not found.', 'error')
            return redirect(url_for('admin_manage_items'))
    elif request.method == 'GET':
        if item:
            return render_template('admin/edit-item.html', item=item)
        else:
            flash('Item not found.', 'error')
            return redirect(url_for('admin_manage_items'))
        
@app.route('/admin/claims')
@login_required
def admin_claims():
    claims = Claim.query.all()  # Adjust the query as needed for your use case
    return render_template('admin/claims.html', claims=claims)

@app.route('/admin/edit-claim/<int:claim_id>', methods=['GET', 'POST'])
@login_required
def edit_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)  # Fetch the claim or show 404 if not found
    if request.method == 'POST':
        # Update the claim's status from the form data
        claim.status = request.form['status']
        db.session.commit()
        flash('Claim updated successfully!', 'success')
        return redirect(url_for('admin_claims'))  # Redirect back to the claims list
    return render_template('admin/edit-claim.html', claim=claim)  # Render a form to edit the claim