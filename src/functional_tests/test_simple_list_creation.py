from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy some of the pokemon games")
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, and now shows both item on his list
        self.wait_for_row_in_list_table("1. Buy a nintendo switch")
        self.wait_for_row_in_list_table("2. Buy some of the pokemon games")

        #Satisfied, he goes back to his work

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Kris starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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