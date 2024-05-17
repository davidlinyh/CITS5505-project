from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
    
    def teardown_method(self):
        self.driver.quit()

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