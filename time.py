import subprocess
import time


package = "Package."
users = "Users."
dashboard = "Dashboard."
site = "Site."
routes = "Routes."


def filter_data(target, data="", final_data=""):
    with open("new.txt", 'r') as file:
        for line in file:
            if target in line:
                final_data = str(line).split(target, 1)[1]
                final_data = final_data[0:final_data.index("\n")]
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
    time_now = time.strftime("%d/%b/%H:%M")
    time_title = time.strftime("%d%b%Hh%Mm")

    with open("data.txt", 'a') as file_new:
        data = compile_data()
        file_new.write("================= new data from %s =================\n" % time_now)
        file_new.write(data)

    subprocess.call("mv new.txt test_on_%s.txt" % time_title)
    subprocess.call("git add .")
    subprocess.call('git commit -m "new_data_"' + time_now)
    subprocess.call("git push origin master")

push_to_git()
