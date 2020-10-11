import json

from data import teachers

x = {}
for i in teachers:
    x[i["id"]] = i

with open("db.json", "w", encoding="utf-8") as g:
    g.writelines(json.dumps(x))
