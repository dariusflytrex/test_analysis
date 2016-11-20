final_data = ""

with open("testing.txt", 'r') as file:
    for line in file:
        if "ok" in line:
            data = str(line).replace(" ... ok (", ":").replace(")", "")
            final_data += data
print final_data