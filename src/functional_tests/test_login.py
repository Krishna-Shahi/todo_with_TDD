from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re

from .base import FunctionalTest

TEST_EMAIL = 'kris@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    def test_get_email_link_to_log_in(self):
        # KRis goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling him to enter his email address, so he does
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, "email").send_keys(Keys.ENTER)

        # A message appears telling him an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, "body").text
        ))

        # He checks his email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        #It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        #he clicks it
        self.browser.get(url)

        #he is logged in!
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "Log out"))
        navbar = self.browser.find_element(By.CSS_SELECTOR,'.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
