# Author: Blake Edwards
# Date: 07/03/2020
import json
import time
db_objs = []
with open("sss.ldjson", 'r', encoding='utf-8') as F:
    for line in F:
        if line != "\n" and len(line) != 12:
            obj = json.loads(line)
            if "docs" in obj:
                for doc in obj["docs"]:
                    db_objs.append(doc)
                    # print(f"-------------------\n{doc}")

print(f"{len(db_objs)} documents parsed")

urls = {}

for obj in db_objs:
    if "verb" and "match" in obj:
        # if obj["verb"] == "delete":
        #     print(obj)
        #     print("-----------------")
        url = obj["match"]
        if url not in urls:
            urls[f"{url}"] = 1
        else:
            urls[f"{url}"] = urls[f"{url}"] + 1
    else:
        db_objs.remove(obj)

print(f"{len(db_objs)} true documents parsed")
print(f"parsed {len(urls)} unique urls")
print("dumping parsed documents to data.json")
with open('data.json', 'w') as f:
    json.dump(db_objs, f)


with open('data.json', 'r') as data_file:
    data = json.load(data_file)

for element in data:
    element.pop('range', None)

with open('data.json', 'w') as f:
    json.dump(data, f)