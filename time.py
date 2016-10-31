import subprocess
import time


package = "Package."
users = "Users."
dashboard = "Dashboard."
site = "AddSite."
routes = "Routes."


def find_time(target, data=""):
    with open("test.txt", 'r') as file:
        for line in file:
            if target in line:
                data += str(line)
    return data.replace(" ", "")


def find_total_time():
    return find_time(package) \
           + find_time(dashboard) \
           + find_time(users) \
           + find_time(site) \
           + find_time(routes)


def push_to_git():
    time_now = time.strftime("%d/%b_%H:%M")
    subprocess.call("git add .")
    print "added"
    subprocess.call('git commit -m "new_data_"' + time_now)
    print "committed"
    subprocess.call("git push origin master")
    print "updated"


def strip_data(test_type, data):
    data = data.split(test_type, 1)[1]
    f = data[0:data.index("\n")]
    file_new.write(f + "\n")
    return data

with open("data.txt", 'a') as file_new:
    data = find_total_time()
    count = data.count("\n")
    while count > 0:
        if package in data:
            data = strip_data(package, data)
        elif users in data:
            data = strip_data(users, data)
        elif dashboard in data:
            data = strip_data(dashboard, data)
        elif site in data:
            data = strip_data(site, data)
        elif routes in data:
            data = strip_data(routes, data)
        count -= 1

push_to_git()
