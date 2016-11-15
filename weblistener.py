import web
import json

urls = ('/.*', 'hooks')
app = web.application(urls, globals())


def process_pull_request(pull_request):
    print "Changing status"
    print pull_request['head']['sha']
    pull_request['head']['sha'] = 'pending'
    print pull_request['head']['sha']


class hooks:
    def POST(self):
        data = web.data()
        parson_json = json.loads(data)
        if "open" in parson_json["action"]:
            print "success"
        if "pull_request" in parson_json["X-GitHub-Event"]:
            process_pull_request(parson_json["pull_request"])


if __name__ == '__main__':
    app.run()