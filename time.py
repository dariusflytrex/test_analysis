import subprocess
import time


package = "Package."
users = "Users."
dashboard = "Dashboard."
site = "Site."
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


def strip_data(test_type, data, file_new):
    info = data.split(test_type, 1)[1]
    i = info[0:info.index("\n")]
    file_new.write(i + "\n")
    return info


def push_to_git():
    time_now = time.strftime("%d/%b/%H:%M")
    time_title = time.strftime("%d%b%Hh%Mm")

    with open("data.txt", 'a') as file_new:
        data = compile_data()
        count = data.count("\n")
        file_new.write("================= new data from %s =================\n" % time_now)
        while count > 0:
            if package in data:
                data = strip_data(package, data, file_new)
            elif users in data:
                data = strip_data(users, data, file_new)
            elif dashboard in data:
                data = strip_data(dashboard, data, file_new)
            elif site in data:
                data = strip_data(site, data, file_new)
            elif routes in data:
                data = strip_data(routes, data, file_new)
            count -= 1

    subprocess.call("mv new.txt test_on_%s.txt" % time_title)
    subprocess.call("git add .")
    subprocess.call('git commit -m "new_data_"' + time_now)
    subprocess.call("git push origin master")


push_to_git()
