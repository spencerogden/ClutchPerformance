import time
import contextlib
import re

import django.contrib.staticfiles.testing
import django.core

from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui
import selenium.webdriver.support.expected_conditions


from django.contrib import auth
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
from factory import DjangoModelFactory, Sequence


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: 'john-doe-{0}@a.com'.format(n))
    username = Sequence(lambda n: '{0}'.format(n))
    password = make_password("password")
    
class ClutchTest(django.contrib.staticfiles.testing.StaticLiveServerTestCase):
    def setUp(self):
        self.browser = selenium.webdriver.Firefox(executable_path='./geckodriver')

    def tearDown(self):
        self.browser.quit()
        
    @contextlib.contextmanager
    def wait_for_page_load(self,timeout=5):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        selenium.webdriver.support.ui.WebDriverWait(self.browser, timeout).until(
            selenium.webdriver.support.expected_conditions.staleness_of(old_page)
            )
            
    def wait_for_condition(self,expected_condition,timeout=5):
        selenium.webdriver.support.ui.WebDriverWait(self.browser, timeout).until(
            expected_condition
            )
        
    
class NewVisitorTest(ClutchTest):
    def test_can_see_hompage(self):
        # Adam hears about a new site and goes to the home page
        self.browser.get(self.live_server_url)

        # Adam sees that the name of the app is ClutchPerformance
        self.assertIn('ClutchPerformance',self.browser.title)

    # Adam reads about the functionality and features 
    def test_can_see_homepage_body(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Hello World Template', self.browser.page_source)
        
    def test_bootstrap_used_for_styling(self):
        self.browser.get(self.live_server_url)
            
        greeting_div = self.browser.find_element_by_id('greeting')
        self.assertAlmostEqual(greeting_div.size['height'],116)
        
# Adam signs up for an account
class userSignup(ClutchTest):
    def test_see_sign_up_link(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text("Sign up")
    
    def test_sign_link(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text("Sign up")
        
        # Adam follows the link
        with self.wait_for_page_load():
            signup_link.click()
            
    def test_sign_form(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text("Sign up")
        
        # Adam follows the link
        with self.wait_for_page_load():
            signup_link.click()
        
        email = self.browser.find_element_by_id('id_email')
        user = self.browser.find_element_by_id('id_username')
        pwd1 = self.browser.find_element_by_id('id_password1')
        pwd2 = self.browser.find_element_by_id('id_password2')
        
        submit = self.browser.find_element_by_id('id_submit')
        
        email.send_keys("adam@example.com")
        user.send_keys("adam")
        pwd1.send_keys("fjrtufjrjtj")
        pwd2.send_keys("fjrtufjrjtj")
        
        with self.wait_for_page_load(timeout=15):
            submit.click()
        
        self.assertIn("Please check your email", self.browser.page_source)
        
    # Adam confirms email address
    def test_validate_email(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text("Sign up")
        
        # Adam follows the link
        with self.wait_for_page_load():
            signup_link.click()
        
        email = self.browser.find_element_by_id('id_email')
        user = self.browser.find_element_by_id('id_username')
        pwd1 = self.browser.find_element_by_id('id_password1')
        pwd2 = self.browser.find_element_by_id('id_password2')
        
        submit = self.browser.find_element_by_id('id_submit')
        
        email.send_keys("adam@example.com")
        user.send_keys("adam")
        pwd1.send_keys("fjrtufjrjtj")
        pwd2.send_keys("fjrtufjrjtj")
        
        with self.wait_for_page_load(timeout=15):
            submit.click()
        
        self.assertIn("Please check your email", self.browser.page_source)
        
        email = django.core.mail.outbox[0]
        
        print('-'*20,email.body)
        
        self.assertIn("adam@example.com", email.to)
        self.assertEqual(email.subject,"Please Activate Your Clutch Account")
        
        self.assertIn("Activate Clutch Account", email.body)
        url_search = re.search(r"http://.+/accounts/activate/[^\s']+",email.body)
        
        if not url_search:
            self.fail("Couldn't find activation url")
        url = url_search.group(0)
        print("URL is",url)
        self.assertIn(self.live_server_url,url)
        
        self.browser.get(url)
        
        self.wait_for_condition(
            lambda s: "activating" in self.browser.page_source
        )
        
        adam_user = User.objects.get(username="adam")
        
        self.assertTrue(adam_user.is_active)
        print(self.browser.current_url)

# Adam logs in
class LoginTest(ClutchTest):
    def test_see_login(self):
        # Adam sees the login link
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text("Log in")
        
    def test_login_link(self):
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text("Log in")
        
        with self.wait_for_page_load():
            login_link.click()
            
        self.assertIn('Clutch',self.browser.title,"Login link goes to wrong page")
    
    def test_login_form(self):
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text("Log in")
        
        with self.wait_for_page_load():
            login_link.click()
            
        user = self.browser.find_element_by_id('id_username')
        pwd = self.browser.find_element_by_id('id_password')
        
    def test_login(self):
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text("Log in")
        
        adam_user = UserFactory.create(
            username='adam',
            password=make_password("fjrtufjrjtj"),
            email='adam@example.com',
            )
        
        with self.wait_for_page_load():
            login_link.click()
            
        user = self.browser.find_element_by_id('id_username')
        pwd = self.browser.find_element_by_id('id_password')
        
        user.send_keys("adam")
        pwd.send_keys("fjrtufjrjtj")
        
        with self.wait_for_page_load():
            pwd.send_keys(Keys.ENTER)
            
        self.assertIn(adam_user.email, self.browser.page_source)
        
       
          

# Adam visits their profile page

# Adam creates a team/organization TeamAlpha

# Adam invites others to the team

# Bob, who is not a member of Clutch, receives an invitation

# Bob uses invitation to go to site and create account

# Bob confirms email address
# Does he need to? Probably since maybe he uses a different email 
# than what the invitation was sent to

# Bob sees that he is a member of TeamAlpha

# Adam sends an invite to Charlie to join TeamAlpha

# Charlie, who is a member, logs in

# Charlie see a notification that he has an invitation to Team Alpha

# Charlie joins TeamAlpha

# Adam makes Charlie a Team Admin

# Adam uploads a text log file to TeamAlpha

# Adam sees the log fil listed in the team files
   