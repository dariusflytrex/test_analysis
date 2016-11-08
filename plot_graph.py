import matplotlib.pyplot as plt

x = []
y = []

with open("data.txt", 'r') as file:
    for line in file:
        if ":" in line:
            x.append(line.split(":", 1)[0])
            y.append(float(line.split(":", 1)[1].strip("s\n")))
    print x
    print y

plt.plot(y)
plt.ylabel("time taken(s)")
plt.xlabel(x)
plt.show()
