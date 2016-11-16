import web
import json
import requests

urls = ('/.*', 'hooks')

app = web.application(urls, globals())
# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'darius@flytrex.com'
PASSWORD = '21730Jie'


class hooks:

    def GET(self):
        parson_json = json.loads(web.data())
        if "pull_request" in parson_json:
            comment_address = parson_json['pull_request']['comments_url']
        # make_github_issue('Test', comment_address, 'The very first try', 'dariusflytrex', None, ['bug'])
        # return "ok"

    def POST(self):
        data = web.data()
        parson_json = json.loads(data)
        # Create our issue
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
        if "pull_request" in parson_json:
            comment_address = parson_json['pull_request']['comments_url']
            session = requests.Session()
            session.auth = (USERNAME, PASSWORD)
            # Add the issue to our repository
            r = session.post(comment_address, json.dumps(issue))
            if r.status_code == 201:
                print 'Successfully created Issue'
            else:
                print 'Could not create Issue'
                print 'Response:', r.content
        return comment_address

if __name__ == '__main__':
    app.run()