import os
import time


def find_time(target, data=""):
    with open("test.txt", 'r') as file:
        for line in file:
            if target in line:
                data += str(line)
    return data.replace(" ", "")


def find_total_time():
    return find_time("Package.") + find_time("Dashboard.") + find_time("Users.") + find_time("AddSite.") + find_time(
        "Routes")


def push_to_git():
    time_now = time.strftime("%d/%b/%H/%M")
    print time_now
    os.popen("git add.")
    print "added"
    os.popen('git commit -m "new_data_"' + 'time_now')
    print "committed"
    os.popen("git push origin master")
    print "updated"

data = find_total_time()
count = data.count("\n")

with open("data.txt", 'a') as file_new:
    while count > 1:
        data = data.split("Package.", 1)[1]
        f = data[0:data.index("\n")]
        file_new.write(f + "\n")
        count -= 1

push_to_git()
