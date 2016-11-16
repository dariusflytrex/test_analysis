import web
import json
import requests

urls = ('/.*', 'hooks')

app = web.application(urls, globals())
# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'darius@flytrex.com'
PASSWORD = '21730Jie'

# The repository to add this issue to
REPO_OWNER = 'dariusflytrex'
REPO_NAME = 'test_analysis'


def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # session = requests.session(auth=(USERNAME, PASSWORD))
    # Create our issue
    issue = {'title': title,
             'body': body,
             'assignee': assignee,
             'milestone': milestone,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content


class hooks:

    def GET(self):
        parson_json = json.loads(web.data())
        header = web.header()
        print header
        action = json.loads(header)
        if 'pull_request' in action['X-GitHub-Event']:
            print action
        pull_request = parson_json['pull_request']
        if 'opened' in parson_json['action']:
            print pull_request['head']['sha']

    def POST(self):
        data = web.data()
        parson_json = json.loads(data)
        pull_request = parson_json['pull_request']
        pull_request['head']['sha'] = 'pending'
        item = {"body": "# Selenium Test Scatter Plot (https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png 'Logo Title Text 1'')"}
        response = requests.post("https://api.github.com/repos/dariusflytrex/test_analysis/pull_request/1", data=item)
        # status = {
        #           'state': 'pending',
        #           }
        return pull_request['base']['repo']['full_name']

if __name__ == '__main__':
    app.run()