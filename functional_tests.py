import unittest
from selenium import webdriver

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

        #He is invited to enter a to-do item straight-away
        self.fail("finish the test!")

        #He types "Buy a nintendo switch" into a text-box
        #(He has been meaning to play games that he couldn't during his childhood)

        #When he hits enter, the page updates and now the page lists
        #"1. Buy a nintendo switch" as an item in a to-do list

        #There is still a text box inviting him to add another item.
        #He enters "Buy some of the pokemon games"

        #The page updates again, and now shows both item on his list

        #Satisfied, he goes back to his work

if __name__ == "__main__":
    unittest.main()