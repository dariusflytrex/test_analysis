#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import sys
import time
import matplotlib.pyplot as plt
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
import numpy as np
import os
import json
import requests

package_header = []
add_mission_cancel = []
add_mission_happy_flow = []
add_mission_missing_param = []
user_header = []
add_site_cancel = []
add_site_happy_flow = []
site_header = []
add_site_missing_param = []
routes_header = []
y = [add_site_cancel, add_site_happy_flow, add_site_missing_param, add_mission_missing_param, add_mission_cancel,
     add_mission_happy_flow, user_header, package_header, site_header, routes_header]
x = ["add_site_cancel", "add_site_happy_flow", "add_site_missing_param", "add_mission_missing_param",
     "add_mission_cancel", "add_mission_happy_flow", "user_header", "package_header", "site_header", "routes_header"]
circle_sha = os.environ.get("CIRCLE_SHA1")
USERNAME = 'darius@flytrex.com'
PASSWORD = 'Asdf1234%'


def plot_graph(test_time, test_name):
    a = np.arange(0, len(test_name))
    plt.plot(a, extract_last_data(test_time), "ro")
    plt.plot(a, find_average(test_time, test_name), "k-")
    for xe, ye in zip(a, test_time):
        plt.scatter([xe] * len(ye), ye)
    plt.title('Selenium Test Timing Scatter Plot')
    xlabel("test names")
    ylabel("time taken(s)")
    plt.xlim((0, len(test_time)+1))
    plt.savefig("test_img/test_%s.png" % circle_sha)


def find_average(test_time, test_name):
    ave = []
    for i in range(len(test_name)):
        average = sum(test_time[i])/float(len(test_time[i]))
        ave.append(average)
        print test_name[i] + ": %.2fs on average." % average
    return ave


def extract_last_data(source):
    extracted = np.arange(0, len(source))
    for i in range(len(source)):
        extracted[i] = source[i][-1]
        del source[i][-1]
    return extracted


def compile_data(final_data=""):
    with open("new.txt", 'r') as file:
        for line in file:
            if "... ok" in line:
                data = str(line).replace(" ... ok (", ":").replace(")", "")
                final_data += data
    return final_data


def updating_data(test_time, test_name):
    time_now = time.strftime("%d/%b/%H/%M")
    with open("data.txt", 'a') as file_new:
        data = compile_data()
        file_new.write("================= new data from %s =================\n" % time_now)
        file_new.write(data)
        for line in file_new:
            for i in range(len(test_name)):
                if test_name[i] in line:
                    test_time[i].append(float(line.split(":", 1)[1].strip("s\n")))


def retrieve_pull_request():
    con = None
    try:
        con = psycopg2.connect("dbname='postgres' user='postgres'")
        cur = con.cursor()
        cur.execute("SELECT * FROM Tests")
        rows = cur.fetchall()
        if circle_sha in rows:
            for row in rows:
                if circle_sha in row:
                    print row
                    return row[2]
        else:
            return None
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()


def post_to_git():
    comment_address = retrieve_pull_request()
    if comment_address:
        issue = {"body": "# Selenium Test Scatter Plot \n\n"
                         "![test](https://github.com/dariusflytrex/test_analysis/blob/darius/test_%s.png?raw=true) \n\n"
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
                         % circle_sha
                 }
        session = requests.Session()
        session.auth = (USERNAME, PASSWORD)
        # Add the issue to our repository
        r = session.post(comment_address, json.dumps(issue))
        if r.status_code == 201:
            print 'Successfully created Issue'
        else:
            print 'Could not create Issue'
            print 'Response:', r.content
    else:
        print "Failed to post comment"

updating_data(y, x)
plot_graph(y, x)
post_to_git()

