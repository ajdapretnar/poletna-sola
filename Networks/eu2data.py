import json
import glob
import os
import csv

header = ["name", "surname", "position", "team"]
writer = csv.DictWriter(open(os.path.join("data", "euro2016.csv"), "w", encoding="utf-8"),
                        fieldnames=header)
writer.writeheader()
for f in glob.glob(os.path.join("data", "euro2016", "players", "*.json")):
    team = os.path.basename(f).split("-")[0]
    team = team.capitalize()
    data = json.loads(open(f, encoding="utf-8").read(), encoding="utf-8")
    players = data["sheets"]["Players"]
    for p in players:
        fullname = p["name"]
        if " " in fullname:
            name, surname = fullname.split(" ")[0], " ".join(fullname.split(" ")[1:])
        else:
            name, surname = "", fullname
        wrow = {"name": name, "position": p["position"], "team": team, "surname": surname,}
        writer.writerow(wrow)

f = os.path.join("data", "euro2016", "teams", "teams.json")
data = json.loads(open(f, encoding="utf-8").read(), encoding="utf-8")
for t in data["sheets"]["Teams"]:
    fullname = t["Coach"]
    if " " in fullname:
        name, surname = fullname.split(" ")[0], " ".join(fullname.split(" ")[1:])
    else:
        name, surname = "", fullname
    wrow = {"name": name, "position": "Coach", "team": t["Team"], "surname": surname,}
    writer.writerow(wrow)
