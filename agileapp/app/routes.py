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
import html

def array_to_string(arr): return json.dumps(arr)
def string_to_array(s): return json.loads(s)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('gallery'))  # Redirect to a useful page post-login

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == html.escape(form.email.data)))
        if user is None:
            flash('User not found. Please register first.', 'info')
            return redirect(url_for('login'))
        if not user.check_password(html.escape(form.password.data)):
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
        return redirect(url_for('gallery'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("enter validation")
        user = User(first_name=html.escape(form.firstname.data), last_name=html.escape(form.lastname.data), email=html.escape(form.email.data))
        user.set_password(html.escape(form.password.data))
        db.session.add(user)
        db.session.commit()
        notify_admin_new_user(user) #NOTIFICATION TO ADMIN ON NEW USER REGISTRATION
        flash('Registration Success! Please Log in to continue.')
        return redirect(url_for('login'))
    print(form.data)
    print(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route('/gallery')
@login_required
def gallery():
    items = LostItem.query.all() # Fetch all lost items from the 
    list_photo_paths = {}
    for item in items:
        list_photo_paths[str(item.id)] = json.loads(item.photo_paths)
        print(json.loads(item.photo_paths)[0])
    # print(list_photo_paths)    
    return render_template('gallery.html', items=items, list_photo_paths=list_photo_paths)

@app.route('/manage-account', methods=['GET', 'POST'])
@login_required
def manage_account():
    if request.method == 'POST':
        # Process form data and update user information
        current_user.first_name = html.escape(request.form['first_name'])
        current_user.last_name = html.escape(request.form['last_name'])
        current_user.email = html.escape(request.form['email'])

        # Handle profile picture update
        

        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    return render_template('manage-account.html', user=current_user)

@app.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = LostItem.query.get_or_404(item_id) # Fetch the item or return 404 if not found
    photo_paths = json.loads(item.photo_paths)
    return render_template('item.html', item_id=item_id, item=item, photo_paths=photo_paths)


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
        return redirect(url_for('gallery'))
    
    form = AddItemForm()
    if form.validate_on_submit():
        print("enter validation")
        item = LostItem(name=html.escape(form.name.data), 
                        description=html.escape(form.description.data), 
                        tags="default_tags", 
                        photo_paths="", 
                        admin_id=current_user.id)
        files = request.files.getlist('photos')
        photo_paths_array = []
        if files  and files[0].filename:
            for index, file in enumerate(files):
                _, file_extension = os.path.splitext(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = secure_filename(timestamp+'_'+str(index)+file_extension)
                file_path = os.path.join(app.config['ITEM_PHOTO_FOLDER'], filename)
                file.save(file_path)
                photo_paths_array.append(filename)
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
            item.name = html.escape(request.form.get('name', item.name))
            item.description = html.escape(request.form.get('description', item.description))
            item.tags = html.escape(request.form.get('tags', item.tags))

            # Handle multiple photos upload
            files = request.files.getlist('photos')
            photo_paths_array = []
            print('filesssssss')
            print(files)
            if files and files[0].filename:
                for index, file in enumerate(files):
                    _, file_extension = os.path.splitext(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = secure_filename(timestamp+'_'+str(index)+file_extension)
                    file_path = os.path.join(app.config['ITEM_PHOTO_FOLDER'], filename)
                    file.save(file_path)
                    photo_paths_array.append(filename)
                item.photo_paths = array_to_string(photo_paths_array)

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
        new_response = request.form.get('admin_response')
        
        print(f"Updating claim {claim_id} with status: {new_status} and response: {new_response}")  # Debugging statement

        claim.status = new_status
        claim.admin_response = new_response  # Update the admin_response field

        if new_status == 'approved':
            update_item_status(claim.item_id)

        db.session.commit()

        notify_user_claim_response(claim)
        flash('Claim status updated successfully.', 'success')
        return redirect(url_for('admin_claims'))

    return render_template('admin/edit-claim.html', claim=claim)

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
        filepath = os.path.join(app.config['ITEM_PHOTO_FOLDER'], filename)
        evidence_photo_path.save(filepath)

    # Create and save the claim
    claim = Claim(
        item_id=item_id,
        claimer_id=current_user.id,
        claimer_description=description,
        evidence_photo_paths=filepath if evidence_photo_path else None,
        status='waiting_approval'
    )
    db.session.add(claim)
    db.session.commit()

    lost_item = LostItem.query.filter_by(id=item_id).first()
    notify_admin_new_claim(lost_item)
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

@app.route('/view-claims')
@login_required
def view_claims():
    user_claims = db.session.query(Claim, LostItem).join(LostItem, Claim.item_id == LostItem.id).filter(Claim.claimer_id == current_user.id).all()
    return render_template('view-claims.html', claims=user_claims)

##################################################################################################################
# Handle Notifications
##################################################################################################################

from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import jsonify
from sqlalchemy import update
from app.models import  Notification
socketio = SocketIO(app)


@app.route('/notification_clicked', methods=['POST'])
def notification_clicked():
    # Perform any necessary operations in response to the notification click
    update_query = update(Notification).where(Notification.user_id == current_user.id, Notification.unread == True).values(unread=False)

    # Execute the update query
    db.session.execute(update_query)
    db.session.commit()  
    # print('clicked');
    return jsonify({'message': 'Notification click handled successfully', 'all_notifications': get_all_notifications(current_user), 'unread_notifications_count':get_unread_notification_count(current_user)})

@app.route('/notification_navbar')
@login_required
def admin_notification_navbar():
    all_notifications =  Notification.query.filter_by(user_id=current_user.id).order_by(Notification.unread.desc(), Notification.created_at.desc()).limit(10).all()
    unread_notifications_count = Notification.query.filter_by(user_id=current_user.id, unread=True).count()
    return render_template('notification_navbar.html', all_notifications = all_notifications, unread_notifications_count=unread_notifications_count)

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated: #
        join_room(current_user.id)  # Join user's room on connect


def notify_user_claim_response(claim):
    user = User.query.filter_by(id=claim.claimer_id).first()

    message = f"Your claim has been {claim.status}."
    notification = Notification(message=message, user_id=user.id, unread=True)
    db.session.add(notification)
    db.session.commit()

    socketio.emit('new_notification', {
        'message': message, 
        'new_notification':message, 
        'unread_notification_count':get_unread_notification_count(user), 
        'all_notifications': get_all_notifications(user),
    }, room=user.id)  # Emit the new notification to the user's room

def notify_admin_new_claim(lost_item):
    alladmins = User.query.filter_by(previlage='admin').all()

    for admin in alladmins:
        message = f"{lost_item.name} has new claim."
        notification = Notification(message=message, user_id=admin.id, unread=True)
        db.session.add(notification)
        db.session.commit()

        socketio.emit('new_notification', {
            'message': message, 
            'new_notification':message, 
            'unread_notification_count':get_unread_notification_count(admin), 
            'all_notifications': get_all_notifications(admin),
        }, room=admin.id)  # Emit the new notification to the admin's room

def notify_admin_new_user(user):
    """
    Create and send notification to all admin about a new user registration.
    """
    alladmins = User.query.filter_by(previlage='admin').all()

    for admin in alladmins:
        message = f"New user {user.email} has registered."
        notification = Notification(message=message, user_id=admin.id, unread=True)
        db.session.add(notification)
        db.session.commit()

        socketio.emit('new_notification', {
            'message': message, 
            'new_notification':message, 
            'unread_notification_count':get_unread_notification_count(admin), 
            'all_notifications': get_all_notifications(admin),
        }, room=admin.id)  # Emit the new notification to the admin's room

def get_unread_notification_count(user):
    return Notification.query.filter_by(user_id=user.id, unread=True).count()


# convert to dictionary
def get_all_notifications(user):
    notifications_query_result = Notification.query.filter_by(user_id=user.id).order_by(Notification.unread.desc(), Notification.created_at.desc()).limit(10).all()
    notifications = [
        {
            'id': n.id,
            'message': n.message,
            'user_id': n.user_id,
            'unread': n.unread,
            'created_at': str(n.created_at),
        }
        for n in notifications_query_result]
    return notifications

