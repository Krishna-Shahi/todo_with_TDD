import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        #Kris has heard about a cool new online To-Do app
        #He goes to checkout it's homepage
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any(row.text == "1. Buy a nintendo switch" for row in rows))

        #There is still a text box inviting him to add another item.
        #He enters "Buy some of the pokemon games"
        self.fail("Finish the test!")

        #The page updates again, and now shows both item on his list

        #Satisfied, he goes back to his work

if __name__ == "__main__":
    unittest.main()