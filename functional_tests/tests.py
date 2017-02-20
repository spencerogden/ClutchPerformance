import django.contrib.staticfiles.testing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import time

def wait(function_with_assertion,timeout=5):
    def modified_fn(*args,**kwargs):
        start_time = time.time()
        while time.time() - start_time > timeout:
            try:
                return function_with_assertion(*args,**kwargs)
            except (AssertionError, WebDriverException) as e:
                time.sleep(0.5)
        return function_with_assertion(*args,**kwargs)
    return modified_fn
    
@wait
def wait_for(function_with_assertion):
    return function_with_assertion()
    
class ClutchTest(django.contrib.staticfiles.testing.StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='./geckodriver')

    def tearDown(self):
        self.browser.quit()
    
class NewVisitorTest(ClutchTest):
    def test_can_see_hompage(self):
        # Adam hears about a new site and goes to the home page
        self.browser.get(self.live_server_url)

        # Adam sees that the name of the app is ClutchPerformance
        wait_for(lambda: self.assertIn('ClutchPerformance',self.browser.title))

    # Adam reads about the functionality and features 
    def test_can_see_homepage_body(self):
        self.browser.get(self.live_server_url)
        wait_for(lambda: self.assertIn('Hello World Template', self.browser.page_source))
        
    def test_bootstrap_used_for_styling(self):
        self.browser.get(self.live_server_url)
        greeting_div = self.browser.find_element_by_id('greeting')
        wait_for(lambda: self.assertAlmostEqual(greeting_div.size['height'],116))
        
# Adam signs up for an account
class userSignup(ClutchTest):
    def test_see_sign_up_link(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text("Sign up")
        
        # Adam follows the link
        signup_link.click()
        
        name = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'id_name'))
        )
        slug = self.browser.find_element_by_id('id_slug')        
        email = self.browser.find_element_by_id('id_email')
        
        name.send_keys("Team Adam")
        slug.send_keys("TeamAdam")
        email.send_keys("adam@example.com")
        
        email.send_keys(Keys.ENTER)
        
        time.sleep(1) # Should be able to elimiate this? TODO
        
        wait_for(lambda: self.assertIn("Thanks!", self.browser.page_source))

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
   