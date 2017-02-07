from selenium import webdriver

browser = webdriver.Firefox(executable_path='./geckodriver')


#  hears about a new site and goes to the home page
browser.get('http://localhost:8000')

# Adam sees that the name of the app is ClutchPerformance
assert 'ClutchPerformance' in browser.title

# Adam reads about the functionality and features 

# Adam signs up for an account

# Adam logs in

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
