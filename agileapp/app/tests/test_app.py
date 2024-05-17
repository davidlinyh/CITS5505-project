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
    #LOGIN PAGE TEST___________________________________________________________________________
    #manage-account PAGE TEST___________________________________________________________________________
    def test_editButton(self):
        self.driver.get("http://localhost:5000/login")
        self.driver.find_element(By.NAME,"email").send_keys("admin1@gmail.com")
        self.driver.find_element(By.NAME,"password").send_keys("123")
        self.driver.find_element(By.NAME,"submit").click()
        
        self.driver.get("http://localhost:5000/manage-account")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "form_button")))
        self.driver.find_element(By.CLASS_NAME,"form_button").click()
        try:
            # Wait for up to 10 seconds for the element to become available
            first_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "first_name")))
            assert first_name.is_displayed()
        except NoSuchElementException:
            print("Test failed: The element was not found") 
    

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

    #REGISTER PAGE TEST___________________________________________________________________________

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
    
