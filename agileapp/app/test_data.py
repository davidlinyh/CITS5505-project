from app import db
from app.models import *
from werkzeug.security import generate_password_hash

#create user data
admin1 = User(
    email = "admin1@gmail.com",
    password_hash = generate_password_hash('123'),
    previlage = "admin",
    first_name = "admin",
    last_name = "one",
    photo_path = 'sample_profile_photo1.jpg',
    created_at = datetime.now(),
    updated_at = datetime.now()
)

admin2 = User(
    email = "admin2@gmail.com",
    password_hash = generate_password_hash('123'),
    previlage = "admin",
    first_name = "admin",
    last_name = "two",
    photo_path = 'sample_profile_photo2.jpg',
    created_at = datetime.now(),
    updated_at = datetime.now()
)

claimer1 = User(
    email = "user1@gmail.com",
    password_hash = generate_password_hash('123'),
    previlage = "claimer",
    first_name = "Antony",
    last_name = "one",
    photo_path = 'sample_profile_photo3.jpg',
    created_at = datetime.now(),
    updated_at = datetime.now(),
)
claimer2 = User(
    email = "user2@gmail.com",
    password_hash = generate_password_hash('123'),
    previlage = "claimer",
    first_name = "Bob",
    last_name = "two",
    photo_path = 'sample_profile_photo4.jpg',
    created_at = datetime.now(),
    updated_at = datetime.now()
)

db.session.add_all([admin1, admin2, claimer1, claimer2])
db.session.commit()


#create lost item data
item1 = LostItem(
    name = "Wallet",
    description = "A black leather wallet, approximately 4 inches in width and 3 inches in height. It contains various cards including credit cards, a driver's license, and membership cards. Additionally, there is a small amount of cash and a family photo inside.",
    tags = "wallet,black,money",
    photo_paths = '["wallet1.jpeg","wallet2.jpeg","wallet3.jpg"]',
    status = "unclaimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin1.id
)
item2 = LostItem(
    name = "Notebook",
    description = "Three small notebooks with colorful covers. Each notebook is approximately 5 inches by 7 inches in size. One of the notebooks is filled with personal thoughts and reflections, another with work-related notes, and the third with sketches and doodles. They hold sentimental value to the owner.",
    tags = "notebook,book,note",
    photo_paths = '["notebook1.jpeg","notebook2.jpeg","notebook3.jpeg"]',
    status = "claimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin2.id
)
item3 = LostItem(
    name = "Laptop",
    description = "A slim, silver laptop with a black keyboard. The laptop is approximately 13 inches in size and is in excellent condition. It was found in a public area and appears to be used for work or study purposes. There are no identifying marks on the laptop, but it likely contains important files and documents.",
    tags = "laptop,computer",
    photo_paths = '["laptop1.jpeg","laptop2.jpeg","laptop3.jpeg"]',
    status = "unclaimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin1.id
)
item4 = LostItem(
    name = "iPad",
    description = "A silver iPad with a black case. The device has a 10.2-inch touchscreen display and appears to be in good condition. It is engraved with initials on the back. The iPad is used for both work and personal purposes and contains important documents, photos, and apps.",
    tags = "iPad,gadget",
    photo_paths = '["ipad1.jpeg","ipad2.jpeg","ipad3.jpeg"]',
    status = "unclaimed",
    created_at = datetime.now(),
    updated_at = datetime.now(),
    admin_id = admin1.id
)

db.session.add_all([item1, item2, item3, item4])
db.session.commit()


#create claim data
claim1 = Claim(
    claimer_description = "I lost my black leather wallet while traveling on the bus yesterday. It is about 4 inches wide and 3 inches tall. Inside, there are several cards, including my driver's license, credit cards, and membership cards. There is also a small amount of cash and a cherished family photo. The wallet holds sentimental value to me, and I would be grateful to have it returned.",
    evidence_photo_paths = '["sample_photo_evidence1.1.jpeg","sample_photo_evidence1.2.jpeg"]',
    admin_response = "We regret to inform you that the found wallet does not match the description provided in your claim. Upon verification, the contents of the wallet do not align with the details provided. We encourage you to continue searching and hope that you recover your lost item soon. If you have any further questions or concerns, please don't hesitate to reach out to us.",
    status = "rejected",
    item_id = item1.id,
    admin_id = admin1.id,
    claimer_id = claimer1.id,
    created_at = datetime.now(),
    updated_at = datetime.now()
)
claim2 = Claim(
    claimer_description = "I misplaced three small notebooks with colorful covers while working in the park yesterday. Each notebook is about 5 inches by 7 inches in size. One of them contains personal thoughts and reflections, another holds work-related notes, and the third is filled with sketches and doodles. These notebooks are essential to my daily life and hold valuable information. I would greatly appreciate their return.",
    evidence_photo_paths = '["sample_photo_evidence2.1.jpeg","2.2"]',
    admin_response = "Good news! The lost notebooks have been positively identified as yours based on the details provided in your claim. We're happy to reunite you with your cherished items. You may collect your notebooks from the lost and found department at your earliest convenience. Your cooperation and patience throughout this process are appreciated.",
    status = "approved",
    item_id = item2.id,
    admin_id = admin2.id,
    claimer_id = claimer2.id,
    created_at = datetime.now(),
    updated_at = datetime.now()
)
claim3 = Claim(
    claimer_description = "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna",
    evidence_photo_paths = '["sample_photo_evidence3.1.jpeg"]',
    admin_response = "Thank you for reaching out regarding the lost wallet. We have received your claim and will compare the details provided with the found item. Please allow us some time to verify the ownership and we will contact you shortly with further instructions on how to proceed.",
    status = "waiting approval",
    item_id = item3.id,
    admin_id = admin2.id,
    claimer_id = claimer2.id,
    created_at = datetime.now(),
    updated_at = datetime.now()
)

db.session.add_all([claim1, claim2, claim3])
db.session.commit()