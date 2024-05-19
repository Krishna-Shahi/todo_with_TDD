import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        test_server = os.environ.get('TEST_SERVER')
        if test_server:
            self.live_server_url = 'http://'+test_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        #Kris has heard about a cool new online To-Do app
        #He goes to checkout it's homepage
        # self.browser.get("http://localhost:8000")
        self.browser.get(self.live_server_url)

        #He notices the page title and header mention to-do lists
        self.assertIn( "To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        #He is invited to enter a to-do item straight-away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        #He types "Buy a nintendo switch" into a text-box
        #(He has been meaning to play games that he couldn't during his childhood)
        inputbox.send_keys("Buy a nintendo switch")

        #When he hits enter, the page updates and now the page lists
        #"1. Buy a nintendo switch" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy a nintendo switch")

        #There is still a text box inviting him to add another item.
        #He enters "Buy some of the pokemon games"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy some of the pokemon games")
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, and now shows both item on his list
        self.wait_for_row_in_list_table("1. Buy a nintendo switch")
        self.wait_for_row_in_list_table("2. Buy some of the pokemon games")

        #Satisfied, he goes back to his work

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Kris starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy a nintendo switch")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy a nintendo switch")

        #He notices that his list has a unique URL
        kris_list_url = self.browser.current_url
        self.assertRegex(kris_list_url, "/lists/.+")

        #Now a new user, Tom, comes along to the site

        ##We delete all the browser's cookies
        ##as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        #Tom vists the home page. There is no sign of Kris' list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy a nintendo switch", page_text)
        self.assertNotIn("pokemon games", page_text)

        #Tom starts a new list by entering a new item. 
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Get milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Get milk")

        #Tom gets his own unique URL
        tom_list_url = self.browser.current_url
        self.assertRegex(tom_list_url, "/lists/.+")
        self.assertNotEqual(tom_list_url, kris_list_url)

        #Again, there is no trace of Kris' list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy a nintendo switch", page_text)
        self.assertIn("Get milk", page_text)

        #Satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        #Kris goes to the home page
        self.browser.get(self.live_server_url)

        #His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        #He notices that the input box is nicely centered
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(inputbox.location["x"]+inputbox.size["width"]/2, 512, delta=10)

        #He starts a new list and sees the input is nicely centered there too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. testing")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(inputbox.location["x"]+inputbox.size["width"]/2, 512, delta=10)