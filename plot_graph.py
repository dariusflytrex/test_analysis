import matplotlib.pyplot as plt
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
import numpy as np

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
ave = []


def find_average(test_time, name):
    average = sum(test_time)/float(len(test_time))
    ave.append(average)
    print name + ": %.2fs on average." % average


def slot_data(line, i):
    timing = float(line.split(":", 1)[1].strip("s\n"))
    y[i].append(timing)


def plot_graph():
    a = np.arange(0, 37, 4)
    plt.xticks(a, x)
    plt.plot(a, y, "k.")
    plt.plot(a, ave, "r-")
    plt.show()
    xlabel("test names")
    ylabel("time taken(s)")
    grid(True)


with open("data.txt", 'r') as file:
    for line in file:
        for i in range(len(x)):
            if x[i] in line:
                slot_data(line, i)

for i in range(len(x)):
    find_average(y[i], x[i])
plot_graph()

