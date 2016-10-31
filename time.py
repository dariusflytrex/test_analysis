import subprocess
import time


package = "Package."
users = "Users."
dashboard = "Dashboard."
site = "AddSite."
routes = "Routes."


def filter_data(target, data=""):
    with open("new.txt", 'r') as file:
        for line in file:
            if target in line:
                data += str(line)
    return data.replace(" ", "")


def compile_data():
    return filter_data(package) \
           + filter_data(dashboard) \
           + filter_data(users) \
           + filter_data(site) \
           + filter_data(routes)


def strip_data(test_type, data):
    info = data.split(test_type, 1)[1]
    i = info[0:info.index("\n")]
    file_new.write(i + "\n")
    return info


def push_to_git():
    time_now = time.strftime("%d/%b/%H:%M")
    time_title = time.strftime("%d%b%Hh%Mm")
    subprocess.call("git add .")
    subprocess.call('git commit -m "new_data_"' + time_now)
    subprocess.call("git push origin master")
    subprocess.call("mv new.txt test_on_%s.txt" %time_title)


with open("data.txt", 'a') as file_new:
    data = compile_data()
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
