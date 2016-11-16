import ast
import json


def process_pull_request(pull_request):
    print "It's %s['title']}"
    print pull_request['head']['sha']
    pull_request['head']['sha'] = 'pending'
    print pull_request['head']['sha']


with open('testing.txt', 'r') as content_file:
    parson_json = json.loads(content_file.read())
    pull = parson_json["action"]
    if pull == "opened":
        process_pull_request(parson_json["pull_request"])



    # for action, status in parson_json.items():
    #     if action == "pull_request":
    #         print status