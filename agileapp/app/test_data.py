from app import db
from app.models import *


#create user data
admin1 = User(
    email = "admin1@gmail.com",
    password_hash = "hashhh",
    previlage = "admin",
    first_name = "admin",
    last_name = "one",
    photo_path = "path////",
    created_at = datetime.now(),
    updated_at = datetime.now()
)

admin2 = User(
    email = "admin2@gmail.com",
    password_hash = "hashhh",
    previlage = "admin",
    first_name = "admin",
    last_name = "two",
    photo_path = "path////",
    created_at = datetime.now(),
    updated_at = datetime.now()
)

claimer1 = User(
    email = "user1@gmail.com",
    password_hash = "hashhh",
    previlage = "claimer",
    first_name = "claimer",
    last_name = "one",
    photo_path = "path////",
    created_at = datetime.now(),
    updated_at = datetime.now(),
)
claimer2 = User(
    email = "user2@gmail.com",
    password_hash = "hashhh",
    previlage = "claimer",
    first_name = "claimer",
    last_name = "two",
    photo_path = "path////",
    created_at = datetime.now(),
    updated_at = datetime.now()
)

db.session.add_all([admin1, admin2, claimer1, claimer2])
db.session.commit()


#create lost item data
item1 = LostItem(
    name = "item1",
    description = "item1 description",
    tags = "tag1,tag2,tag3",
    photo_paths = "path////",
    status = "unclaimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin1.id
)
item2 = LostItem(
    name = "item2",
    description = "item2 description",
    tags = "tag1,tag2,tag3",
    photo_paths = "path////",
    status = "claimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin2.id
)
item3 = LostItem(
    name = "item3",
    description = "item3 description",
    tags = "tag1,tag2,tag3",
    photo_paths = "path////",
    status = "unclaimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin1.id
)

db.session.add_all([item1, item2, item3])
db.session.commit()


#create claim data
claim1 = Claim(
    claimer_description = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna",
    evidence_photo_paths = "path////",
    admin_response = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna",
    status = "rejected",
    item_id = item1.id,
    admin_id = admin1.id,
    claimer_id = claimer1.id,
    created_at = datetime.now(),
    updated_at = datetime.now()
)
claim2 = Claim(
    claimer_description = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna",
    evidence_photo_paths = "path////",
    admin_response = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna",
    status = "approved",
    item_id = item2.id,
    admin_id = admin2.id,
    claimer_id = claimer2.id,
    created_at = datetime.now(),
    updated_at = datetime.now()
)

db.session.add_all([claim1, claim2])
db.session.commit()