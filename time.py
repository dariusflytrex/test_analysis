import subprocess
import time
import matplotlib.pyplot as plt
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
import numpy as np


package = "Package."
users = "Users."
dashboard = "Dashboard."
site = "Site."
routes = "Routes."
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


def plot_graph(test_time, test_name):
    a = np.arange(0, len(test_time))
    plt.plot(a, find_average(test_time, test_name), "k-")
    plt.plot(a, extract_last_data(test_time), "ro")
    plt.plot(a, test_time, "b.")
    # txt = '''
    # 1: add_site_cancel 2: add_site_happy_flow 3: add_site_missing_param 4: add_mission_missing_param
    # 5: add_mission_cancel 6: add_mission_happy_flow 7: user_header 8: package_header
    # 9: site_header 10: routes_header
    #
    # '''
    # plt.text(.1, .1, txt)
    plt.title('Selenium Test Timing Scatter Plot')
    xlabel("test names")
    ylabel("time taken(s)")
    # plt.xlim((-1, len(test_time)1))
    plt.savefig("test.png")


def extract_data(test_time, test_name):
    with open("data.txt", 'r') as file:
        for line in file:
            for i in range(len(test_name)):
                if test_name[i] in line:
                    test_time[i].append(float(line.split(":", 1)[1].strip("s\n")))


def filter_data(target, final_data=""):
    with open("new.txt", 'r') as file:
        for line in file:
            if target in line:
                data = str(line).split(target, 1)[1]
                data = data[0:data.index("\n")]
                final_data += data + "\n"
    return final_data.replace(" ", "")


def compile_data():
    data = filter_data(package) \
           + filter_data(dashboard) \
           + filter_data(users) \
           + filter_data(site) \
           + filter_data(routes)
    return data


def push_to_git():
    time_now = time.strftime("%d/%b/%H/%M")
    time_title = time.strftime("%d%b%Hh%Mm")

    with open("data.txt", 'a') as file_new:
        data = compile_data()
        file_new.write("================= new data from %s =================\n" % time_now)
        file_new.write(data)

    subprocess.call("mv new.txt test_on_%s.txt" % time_title)
    subprocess.call("git add data.txt test.png")
    subprocess.call('git commit -m "newdata_"' + time_now)
    subprocess.call("git push origin master")


push_to_git()
extract_data(y, x)
plot_graph(y, x)
