import os
import json

from data import teachers

x={}
for i in teachers:
    x[i["id"]]=i

if not os.path.isfile("db.json"):
    with open("db.json", "w", encoding="utf-8") as g:
        g.writelines(json.dumps(x))

