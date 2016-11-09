import matplotlib.pyplot as plt

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


def findAverage(test, name):
    average = sum(test) / float(len(test))
    print name + ": %.2fs on average." % average


with open("data.txt", 'r') as file:
    for line in file:
        if "package_header" in line:
            package_header.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_mission_cancel" in line:
            add_mission_cancel.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_mission_happy_flow" in line:
            add_mission_happy_flow.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_mission_missing_param" in line:
            add_mission_missing_param.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "user_header" in line:
            user_header.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_site_cancel" in line:
            add_site_cancel.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_site_happy_flow" in line:
            add_site_happy_flow.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "site_header" in line:
            site_header.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "add_site_missing_param" in line:
            add_site_missing_param.append(float(line.split(":", 1)[1].strip("s\n")))
        elif "routes_header" in line:
            routes_header.append(float(line.split(":", 1)[1].strip("s\n")))
    findAverage(package_header, "package_header")
    findAverage(add_site_happy_flow, "add_site_happy_flow")
    findAverage(add_site_missing_param, "add_site_missing_param")
    findAverage(add_site_cancel, "add_site_cancel")

#
#         if ":" in line:
#             x.append(line.split(":", 1)[0])
#             y.append(float(line.split(":", 1)[1].strip("s\n")))
#     print x
#     print y
#
# plt.plot(y)
# plt.ylabel("time taken(s)")
# plt.xlabel(x)
# plt.show()
