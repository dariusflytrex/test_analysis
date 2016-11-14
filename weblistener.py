import web
import os
import json

urls = ('/.*', 'hooks')

app = web.application(urls, globals())

class hooks:
    def POST(self):
        data = web.data()
        pull_request = data.get("pull_request")
        if "open" in pull_request:
            print "YES"
            pull_request["locked"] = True
        print data
        print "++++++++++++++++++++++++++++++++++++Pull request processed!"
        return 'OK'

if __name__ == '__main__':
    app.run()