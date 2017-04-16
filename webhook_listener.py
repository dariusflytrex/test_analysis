#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import web
import json


urls = ('/.*', 'hooks')

app = web.application(urls, globals())
# Authentication for user filing issue (must have read/write access to


def store_config(sha, pull_number):
        con = None
        try:
            con = psycopg2.connect("dbname='testdb' user='darius'")
            cur = con.cursor()
            cur.execute("INSERT INTO Tests VALUES(1,%s, %s)") % sha, pull_number
            con.commit()

        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print 'Error %s' % e
            sys.exit(1)

        finally:
            if con:
                con.close()


class hooks:

    def POST(self):
        data = web.data()
        parson_json = json.loads(data)
        if "pull_request" in parson_json:
            comment_address = parson_json['pull_request']['comments_url']
            store_config("abddd", comment_address)
        else:
            return "it's not a pull request"
        return "pull request received"

if __name__ == '__main__':
    app.run()