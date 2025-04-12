from json import load, dump

data = load(open("data.json"))

while True:
    print(data)
    cmd=input("Command: ")
    if cmd == "exit":
        break
    elif cmd == "add":
        name = input("Name: ").lower()
        ing = input("Ingredient: ").lower()
        if ing != "":
            frm = input("From: ").lower()
        else:
            data[name] = []
            continue

        if frm not in data:
            data[frm] = []
        data[frm].append((name, ing))

        if name not in data:
            data[name] = []
        # print(data)
    elif cmd == "save":
        dump(data, open("data.json", "w"))
print("Exiting")
dump(data, open("data.json", "w"))
# print(data)
exit()