import requests
import json

USERNAME = 'darius@flytrex.com'
PASSWORD = 'Asdf1234%'

issue = {"body": "# Selenium Test Scatter Plot \n\n"
                 "![test](https://github.com/dariusflytrex/test_analysis/blob/darius/test.png?raw=true) \n\n"
                 "Number | Test names \n "
                 "--------|-------- \n"
                 "0 | add_site_cancel \n"
                 "1 | add_site_happy_flow\n"
                 "2 | add_site_missing_param\n"
                 "3 | add_mission_missing_param\n"
                 "4 | add_mission_cancel\n"
                 "5 | add_mission_happy_flow\n"
                 "6 | user_header\n"
                 "7 | package_header\n"
                 "8 | site_header\n"
                 "9 |routes_header\n"
         }
session = requests.Session()
session.auth = (USERNAME, PASSWORD)
# Add the issue to our repository
r = session.post("https://api.github.com/repos/dariusflytrex/test_analysis/issues/9/comments", json.dumps(issue))
if r.status_code == 201:
    print 'Successfully created Issue'
else:
    print 'Could not create Issue'
    print 'Response:', r.content