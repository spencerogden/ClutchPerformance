import time
import contextlib

import django.contrib.staticfiles.testing

from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui
import selenium.webdriver.support.expected_conditions


    
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
        
        # Adam follows the link
        with self.wait_for_page_load():
            signup_link.click()
        
        name = self.browser.find_element_by_id('id_name')
        slug = self.browser.find_element_by_id('id_slug')        
        email = self.browser.find_element_by_id('id_email')
        
        name.send_keys("Team Adam")
        slug.send_keys("TeamAdam")
        email.send_keys("adam@example.com")
        
        with self.wait_for_page_load():
            email.send_keys(Keys.ENTER)
        
        self.assertIn("Thanks!", self.browser.page_source)

# Adam logs in
class LoginTest(ClutchTest):
    def test_login(self):
        # Adam sees the login link
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text("Log in")
        
        
        
# Adam confirms email address

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
   