import os
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException


class Test:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
    
    def teardown_method(self):
        self.driver.quit()

    #Function/method names should be sufficient to understand the test case undertaken.
    #ITEM CLAIM TEST_____________________________________________________________________________________
'''
    def test_itemClaim(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        notebook_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[h3[text()='Notebook']]")))
        view_details_link = notebook_div.find_element(By.LINK_TEXT, "View Details")
        view_details_link.click()

        claimItem_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "claimBtn")))
        claimItem_button.click()

        description = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "claimer_description")))
        description.send_keys("These notebooks are mine. I left them in the class.")

        submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
        submit_button.click()

        self.driver.get("http://localhost:5000/view-claims")

        table_rows = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
        claimed_item_found = False
        for row in table_rows:
            if "Notebook" in row.text: 
                claimed_item_found = True
        
        assert claimed_item_found
'''
    #GALLERY PAGE TEST___________________________________________________________________________________
'''
    #Checking for the first item
    def test_viewDetailsButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        view_details_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[1]//a[contains(text(), 'View Details')]")))
        view_details_link.click()

        assert self.driver.current_url == "http://localhost:5000/item/1"
'''
    #CONTACT BUTTON (located in the footer of all pages) TEST_________________________
'''   
    def test_contactButton(self):
        self.driver.get("http://localhost:5000/login")

        contact_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='contact us']")))
        current_window_handle = self.driver.current_window_handle
        contact_button.click()

        new_window_handle = [handle for handle in self.driver.window_handles if handle != current_window_handle][0]
        self.driver.switch_to.window(new_window_handle)

        assert self.driver.current_url == "https://www.uwastudentguild.com/contact"
'''
    #ADMIN: NAV BAR TEST_________________________________________________________________________________
'''
    def test_galleryButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        #After logging in as an admin, we land on gallery page. So, going to manage account page for testing purposes
        self.driver.get("http://localhost:5000/manage-account")

        gallery_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Gallery']")))
        gallery_button.click()

        assert self.driver.current_url == "http://localhost:5000/gallery"
    
    def test_claimsButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        claims_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Claims']")))
        claims_button.click()

        assert self.driver.current_url == "http://localhost:5000/admin/claims"

    def test_newItemButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        newItem_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='New Item']")))
        newItem_button.click()

        assert self.driver.current_url == "http://localhost:5000/admin/new-item"

    def test_manageItemsButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        manageItems_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Manage Items']")))
        manageItems_button.click()

        assert self.driver.current_url == "http://localhost:5000/admin/manage-items"
    
    def test_profileButton_firstButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        dropdown_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropdown")))
        dropdown_button.click()

        manage_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Manage Account']")))
        manage_button.click()

        assert self.driver.current_url == "http://localhost:5000/manage-account"

    def test_profileButton_secondButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        dropdown_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropdown")))
        dropdown_button.click()

        logout_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log Out']")))
        logout_button.click()

        assert self.driver.current_url == "http://localhost:5000/login"
    
'''
    #USER: NAV BAR TEST__________________________________________________________________________________
'''
    def test_galleryButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user2@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        #After logging in as an user, we land on gallery page. So, going to manage account page for testing purposes
        self.driver.get("http://localhost:5000/manage-account")

        gallery_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Gallery']")))
        gallery_button.click()

        assert self.driver.current_url == "http://localhost:5000/gallery"

    def test_claimsButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        claims_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Claims']")))
        claims_button.click()

        assert self.driver.current_url == "http://localhost:5000/view-claims"

    def test_profileButton_firstButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user2@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        dropdown_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropdown")))
        dropdown_button.click()

        manage_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Manage Account']")))
        manage_button.click()

        assert self.driver.current_url == "http://localhost:5000/manage-account"

    def test_profileButton_secondButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user2@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        dropdown_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropdown")))
        dropdown_button.click()

        logout_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log Out']")))
        logout_button.click()

        assert self.driver.current_url == "http://localhost:5000/login"
'''
    #MANAGE-ACCOUNT PAGE TEST___________________________________________________________________________
'''    
    def test_editButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()
        
        self.driver.get("http://localhost:5000/manage-account")
        edit_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Edit']")))
        edit_button.click()
        try:
            # Wait for up to 10 seconds for the element to become available
            first_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "first_name")))
            assert first_name.is_displayed()
        except NoSuchElementException:
            print("Test failed: The element was not found") 
    
    def test_cancelButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        self.driver.get("http://localhost:5000/manage-account")
        edit_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Edit']")))
        edit_button.click()

        try:
            # Wait for up to 10 seconds for the element to become available
            cancel_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Cancel']")))
            cancel_button.click()
            assert WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Edit']"))) 
        except NoSuchElementException:
            print("Test failed: The element was not found") 

    def test_reflectionOfEdits(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("user2@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

        self.driver.get("http://localhost:5000/manage-account")
        edit_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Edit']")))
        edit_button.click()

        # Path to the folder containing photos
        photos_folder = r''

        # Sample data for other fields
        first_names = ["Alice", "Bob", "Charlie", "Diana"]
        last_names = ["Smith", "Johnson", "Williams", "Brown"]
        emails = ["example1@gmail.com", "example2@gmail.com", "example3@gmail.com", "example4@gmail.com"]
        passwords = ["$123","#123","!123","@123"]

        # Function to get random data
        def get_random_data():
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = random.choice(emails)
            password = random.choice(passwords)
            return first_name, last_name, email, password
        
        # Function to select a random photo
        def get_random_photo(folder_path):
            photos = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            return os.path.join(folder_path, random.choice(photos))
        
        # Get random data for other fields
        first_name, last_name, email, password = get_random_data()

        # Get a random photo from the folder
        random_photo_path = get_random_photo(photos_folder)
        
        # Find form fields and fill them with random data
        first_name_input = self.driver.find_element(By.ID, "first_name")
        last_name_input = self.driver.find_element(By.ID, "last_name")
        email_input = self.driver.find_element(By.ID, "email")
        new_password_input = self.driver.find_element(By.ID, "new_password")
        file_input = self.driver.find_element(By.ID, "photo_path")
        
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        email_input.clear()
        email_input.send_keys(email)
        new_password_input.clear()
        new_password_input.send_keys(password)
        file_input.send_keys(random_photo_path)

        #Save the changes
        save_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        save_button.click()

        changed_email_input = self.driver.find_element(By.ID,'email')

        flag = False

        if email == changed_email_input.get_attribute('value'): flag = True

        self.revert_to_old_data(email="user2@gmail.com",password="123")

        assert flag
    
    def revert_to_old_data(self, email, password):

        # Revert back to old data for subsequent tests
        edit_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Edit']")))
        edit_button.click()

        # Find form fields and fill them with old data
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "new_password")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        # Save the changes
        save_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        save_button.click()

'''        
    #LOGIN PAGE TEST___________________________________________________________________________         
'''
    def test_login_correctCredentials(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()
        
        #Wait for change of URL
        WebDriverWait(self.driver,10).until(EC.url_changes("http://localhost:5000/login"))

        #Checking current URL
        assert self.driver.current_url == "http://localhost:5000/gallery"
    
    def test_login_wrongCreddentials(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("1234")
        self.driver.find_element(By.NAME,"submit").click()

        #Wait for error message
        error_message = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"flashes")))

        #Check if the error message gets displayed
        assert any("Invalid password" in error.text for error in error_message)

    def test_login_invalidEmail(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()

         # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Invalid email address.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")

    def test_login_unregistered(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh1999@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("1234")
        self.driver.find_element(By.NAME,"submit").click()

        #Wait for error message
        error_message = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"flashes")))

        #Check if the error message gets displayed
        assert any("User not found. Please register first." in error.text for error in error_message)
'''
    #REGISTER PAGE TEST___________________________________________________________________________
'''
    def test_register_newuser(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh Sundaram")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh1999@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"submit").click()

        #Wait for change of URL
        WebDriverWait(self.driver,10).until(EC.url_changes("http://localhost:5000/register"))
        
        #Wait for registration success message 
        success_message = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"flashes")))
        
        #Checking current URL and check if registration success message is displayed
        assert self.driver.current_url == "http://localhost:5000/login" and any("Registration Success! Please Log in to continue." in message.text for message in success_message)
    
    def test_register_invalidName(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh@")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar$")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh1999@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"submit").click()

        # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Invalid characters. Use only characters and whitespaces.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")

    def test_register_exisitingEmail(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh136@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"submit").click()

        # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Email already registered. Please use a different email address.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")
    
    def test_register_invalidEmail(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh136gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"submit").click()

        # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Invalid email address.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")
    
    def test_register_passwordMismatch(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh11223344@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("$123Adharsh")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("$124Adharsh")
        self.driver.find_element(By.NAME,"submit").click()

        # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Field must be equal to password.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")

    def test_register_shortPassword(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh11223344@gmail.com")
        short_password="$123Ad"
        self.driver.find_element(By.NAME,"password").send_keys(short_password)
        self.driver.find_element(By.NAME,"confirm_password").send_keys(short_password)
        self.driver.find_element(By.NAME,"submit").click()

         # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", f'//div[contains(text(), "Please lengthen this text to 8 characters or more (you are currently using {len(short_password)} characters).")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")
    
    def test_register_noSpecialCharacterPassword(self):
        self.driver.get("http://localhost:5000/register")
        self.driver.find_element(By.NAME,"firstname").send_keys("Adharsh")
        self.driver.find_element(By.NAME,"lastname").send_keys("Soudakar")
        self.driver.find_element(By.NAME,"email").send_keys("adharsh11223344@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("12345678")
        self.driver.find_element(By.NAME,"confirm_password").send_keys("12345678")
        self.driver.find_element(By.NAME,"submit").click()

         # Check if the validation error message is displayed
        try:
            error_message = self.driver.find_element("xpath", '//div[contains(text(), "Password should contain atleast one special charater.")]')
            assert error_message is not None
            print("Test passed")
        except NoSuchElementException:
            print("Test failed: Validation error message not displayed")
''' 
    
