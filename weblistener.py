import web

urls = ('/.*', 'hooks')

app = web.application(urls, globals())

class hooks:
    def POST(self):
        data = web.data()
        if "pull_request" in data:
            print "YES"
        print '\nDATA RECEIVED:'
        print data
        print
        return 'OK'

if __name__ == '__main__':
    app.run()