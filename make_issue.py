import json
import requests

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'darius@flytrex.com'
PASSWORD = '21730Jie'

# The repository to add this issue to
REPO_OWNER = 'dariusflytrex'
REPO_NAME = 'test_analysis'
PULL_REQUEST = 5


def make_github_issue(title, body=None, assignee=None, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (REPO_OWNER, REPO_NAME, PULL_REQUEST)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # session = requests.session(auth=(USERNAME, PASSWORD))
    # Create our issue
    issue = {
        # 'title': title,
             'body': body,
             # 'assignee': assignee,
             # 'milestone': milestone,
             # 'labels': labels
             }
    # issue = {"body": "Nice change",
    #          # "in_reply_to": 0,
    #          "commit_id": "23e468b7adc94518a5aee1086690b798b7077f0c",
    #          "path": "listener.py",
    #          "position": 4
    #          }
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    commenting = session.get(url)
    print commenting
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content

make_github_issue('Test', 'Test', 'dariusflytrex', None, ['bug'])

original = "https://github.com/Flytrex/delivery_server/pull/55"
needed = "https://api.github.com/repos/Flytrex/delivery_server/issues/55"
v1 = original.replace("://", "://api.").replace("Flytrex", "repos/Flytrex").replace("pull", "issues")

#send files using request:
r = requests.post('http://httpbin.org/post', files={'report.xls': open('report.xls', 'rb')})