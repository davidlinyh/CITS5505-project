from urllib.parse import urlsplit
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from datetime import datetime
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddItemForm
from app.models import User, LostItem, Claim
import os
import json

def array_to_string(arr): return json.dumps(arr)
def string_to_array(s): return json.loads(s)

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
    items = LostItem.query.all() # Fetch all lost items from the database
    return render_template('gallery.html', items=items)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

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
    item = LostItem.query.get_or_404(item_id) # Fetch the item or return 404 if not found
    return render_template('item.html', item_id=item_id, item=item)


@app.route('/admin/index')
@app.route('/admin')
@login_required
def admin_index():
    if current_user.previlage != 'admin':
        return redirect(url_for('index'))
    
    recent_items = LostItem.query.order_by(LostItem.created_at.desc()).limit(5).all()
    recent_claims = db.session.query(Claim, User, LostItem)\
                              .join(User, User.id == Claim.claimer_id)\
                              .join(LostItem, LostItem.id == Claim.item_id)\
                              .order_by(Claim.created_at.desc())\
                              .limit(5)\
                              .all()
    return render_template('admin/index.html', recent_items=recent_items, recent_claims=recent_claims)

@app.route('/admin/manage-items', methods=['GET']) 
@login_required
def admin_manage_items(): 
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))
    items = LostItem.query.all() # Fetch all lost items from the database
    return render_template('admin/manage-items.html', items=items)

@app.route('/admin/new-item', methods=['GET', 'POST'])
@login_required
def new_item():
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))
    
    form = AddItemForm()
    if form.validate_on_submit():
        print("enter validation")
        item = LostItem(name=form.name.data, 
                        description=form.description.data, 
                        tags="default_tags", 
                        photo_paths="", 
                        admin_id=current_user.id)
        files = request.files.getlist('photos')
        photo_paths_array = []
        if files:
            for index, file in enumerate(files):
                _, file_extension = os.path.splitext(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = secure_filename(timestamp+'_'+str(index)+file_extension)
                file_path = os.path.join(app.config['ITEM_PHOTO_FOLDER'], filename)
                file.save(file_path)
                photo_paths_array.append(file_path)
            item.photo_paths = array_to_string(photo_paths_array)

        db.session.add(item)
        db.session.commit()

        return redirect(url_for('admin_manage_items'))

    return render_template('/admin/new-item.html', form=form)

@app.route('/admin/edit-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_item(item_id):
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))
    
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
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))
    
    claims = db.session.query(Claim, User, LostItem).join(User, User.id == Claim.claimer_id).join(LostItem, LostItem.id == Claim.item_id).all()
    return render_template('admin/claims.html', claims=claims)

@app.route('/admin/edit-claim/<int:claim_id>', methods=['GET', 'POST'])
@login_required
def edit_claim(claim_id):
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))
    
    claim = Claim.query.get_or_404(claim_id)
    if request.method == 'POST':
        new_status = request.form.get('status')
        claim.status = new_status
        if new_status == 'Approved':
            update_item_status(claim.item_id)
        db.session.commit()
        flash('Claim status updated successfully.', 'success')
        return redirect(url_for('admin_claims'))

    return render_template('/admin/edit-claim.html', claim=claim)

def update_item_status(item_id):
    item = LostItem.query.get(item_id)
    if item:
        item.status = 'claimed'
        db.session.commit()

@app.route('/submit-claim', methods=['POST'])
def submit_claim():
    if not current_user.is_authenticated:
        flash('You need to log in to submit a claim.', 'info')
        return redirect(url_for('login'))

    item_id = request.form['item_id']
    description = request.form['claimer_description']
    evidence_photo_path = request.files['evidence_photo_paths']

    # Process and save the evidence photo
    if evidence_photo_path:
        filename = secure_filename(evidence_photo_path.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        evidence_photo_path.save(filepath)

    # Create and save the claim
    claim = Claim(
        item_id=item_id,
        claimer_id=current_user.id,
        claimer_description=description,
        evidence_photo_paths=filename if evidence_photo_path else None,
        status='waiting_approval'
    )
    db.session.add(claim)
    db.session.commit()

    flash('Your claim has been submitted successfully.', 'success')
    return redirect(url_for('item', item_id=item_id))  # Redirect back to the item page

@app.route('/admin/delete-item/<int:item_id>', methods=['POST'])
@login_required
def admin_delete_item(item_id):
    if not current_user.previlage == 'admin':
        return redirect(url_for('index'))

    item = LostItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('admin_manage_items'))
