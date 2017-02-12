from selenium import webdriver
import unittest

class ClutchTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='./geckodriver')

    def tearDown(self):
        self.browser.quit()
    
class NewVisitorTest(ClutchTest):
    def test_can_see_hompage(self):
        # Adam hears about a new site and goes to the home page
        self.browser.get('http://localhost:8000')

        # Adam sees that the name of the app is ClutchPerformance
        assert 'ClutchPerformance' in self.browser.title, "Browser title was: " + self.browser.title

    # Adam reads about the functionality and features 
    def test_can_see_homepage_body(self):
        self.browser.get('http://localhost:8000')
        assert 'Hello World Template' in self.browser.page_source
        
    def test_bootstrap_used_for_styling(self):
        self.browser.get('http://localhost:8000')
        greeting_div = self.browser.find_element_by_id('greeting')
        self.assertAlmostEqual(greeting_div.size['height'],116)
        
# Adam signs up for an account

# Adam logs in
class LoginTest(ClutchTest):
    def test_see_login_link(self):
        self.browser.get('http://localhost:8000')
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

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    
    