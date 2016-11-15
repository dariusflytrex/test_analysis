import web
import json
import requests

urls = ('/.*', 'hooks')

app = web.application(urls, globals())

ACCESS_TOKEN = '24f2fa4a7347afeac50ffca8414bd491a040e428'


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
        response = requests.post("https://api.github.com/repos/dariusflytrex/test_analysis/hooks", data=pull_request,
                                 headers={'Content-Type': 'application/json'}
                                 )
        # status = {
        #           'state': 'pending',
        #           }
        return pull_request['base']['repo']['full_name']



if __name__ == '__main__':
    app.run()