from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys

class TestIndexPage(StaticLiveServerTestCase):

    def setUp(self):
        """ Set up the Selenium WebDriver """
        self.driver = webdriver.Chrome()

    def tearDown(self):
        """ Close the Selenium WebDriver """
        self.driver.quit()

    def test_index_page_loads(self):
        """ Test that the index page loads and contains a specific element """
        self.driver.get(self.live_server_url)
        self.assertIn("No polls are available.", self.driver.page_source)

    def test_question_submission(self):
        """ Test submitting a question form and verifying the response """
        self.driver.get(self.live_server_url)
        input_box = self.driver.find_element_by_name("question_text")
        input_box.send_keys("¿Cuál es tu comida favorita?")
        input_box.send_keys(Keys.RETURN)
        self.assertIn("¿Cuál es tu comida favorita?", self.driver.page_source)
