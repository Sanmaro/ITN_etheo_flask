import requests
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Change in production
BASE_URL = "http://localhost:5000"

class BaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = BASE_URL
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def get_full_url(self, endpoint):
        return f"{self.base_url}{endpoint}"


class TestHomePage(BaseTest):

    def setUp(self):
        path = super().get_full_url("")
        self.driver.get(path)

    def test_home_nav(self):
        nav = self.driver.find_element(By.TAG_NAME, "nav")
        self.assertIsNotNone(nav)

        # All links present?
        expected_links = ["Insurances", "Testimonials", "Contact"]
        nav_links = self.driver.find_elements(By.XPATH, "//div[@class='navbar-nav mt-2']/a/h3")
        found_links = [link.get_attribute("innerHTML") for link in nav_links]
        for expected_link in expected_links:
            self.assertIn(expected_link, found_links)

        # No broken links?
        nav_links = self.driver.find_elements(By.TAG_NAME, "a")
        for link in nav_links:
            href = link.get_attribute("href")
            response = requests.head(href)
            self.assertTrue(response.status_code == 200, f"Failed URL: {href}")

        # Does navbar wraps up on small screens?
        self.driver.set_window_size(320, 480)
        toggle = self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
        self.assertTrue(toggle.is_displayed())

    def test_home_footer(self):
        footer = self.driver.find_element(By.TAG_NAME, "footer")
        self.assertIsNotNone(footer)
        self.assertIn("Vojtěch Ettler", footer.text)

    def test_home_content(self):
        content = self.driver.find_element(By.TAG_NAME, "body")
        self.assertIn("Welcome to Etheo Insurance", content.text)



class TestLoginPage(BaseTest):

    def setUp(self):
        path = super().get_full_url("/login")
        self.driver.get(path)

    def test_valid_login(self):
        email = self.driver.find_element(By.NAME, "login_email")
        password = self.driver.find_element(By.NAME, "login_password")
        email.send_keys("ester@etheo.cz")
        password.send_keys("mamradetheo")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        expected_url = self.get_full_url("/my_insurances")
        self.assertEqual(self.driver.current_url, expected_url)
        message = self.driver.find_element(By.XPATH, "//div[@role='alert']")
        self.assertIn("You have successfully logged in!", message.text)

    def test_invalid_login(self):
        email = self.driver.find_element(By.NAME, "login_email")
        password = self.driver.find_element(By.NAME, "login_password")
        email.send_keys("invalid@etheo.cz")
        password.send_keys("invalid")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        message = self.driver.find_element(By.XPATH, "//div[@role='alert']")
        self.assertIn("Invalid e-mail address or password.", message.text)


# TO BE EXTENDED

if __name__ == "__main__":
    unittest.main()
