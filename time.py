def find_time(target, data=""):
    with open("test.txt", 'r') as file:
        for line in file:
            if target in line:
                data += str(line)
    return data.replace(" ", "")


def find_total_time():
    return find_time("Package.") + find_time("Dashboard.") + find_time("Users.") + find_time("AddSite.") + find_time(
        "Routes")

data = find_total_time()
count = data.count("\n")

while count > 0:
    data = data.split("Package.", 1)[1]
    f = data[0:data.index("\n")]
    print f
    count -= 1
