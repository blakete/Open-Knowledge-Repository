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
# processing before adding to DB
db_objs = [x for x in db_objs if 'verb' in x] 
for obj in db_objs:
    url = obj["match"]
    if url not in urls:
        urls[f"{url}"] = 1
    else:
        urls[f"{url}"] = urls[f"{url}"] + 1
    # remove unecessary fields
    obj.pop('range', None)
    obj.pop('v', None)
    obj.pop('_rev', None)
    if "className" in obj:
        if "cyan" in obj['className']:
            obj['className'] = "cyan"
        elif "yellow" in obj['className']:
            obj['className'] = "yellow"
        elif "red" in obj['className']:
            obj['className'] = "red"
# collect all deleted document ids
del_ids = []
for obj in db_objs:
    if "delete" in obj['verb']:
        del_ids.append(obj['correspondingDocumentId'])
# delete all documents with corresponding ids
db_objs = [x for x in db_objs if not 'delete' in x['verb']]
db_objs = [x for x in db_objs if '_id' in x and x['_id'] not in del_ids]
for obj in db_objs:
    if "_id" in obj:
        obj['highlight_id'] = obj.pop('_id')
    if "match" in obj:
        obj['url'] = obj.pop('match')
print(f"{len(db_objs)} true documents parsed")
print(f"parsed {len(urls)} unique urls")
print("dumping parsed documents to data.json")
with open('data.json', 'w') as f:
    json.dump(db_objs, f)

# insert documents into elastic search database
import requests, json, os
from elasticsearch import Elasticsearch
res = requests.get('http://localhost:9200')
print (res.content)
res = requests.get("http://localhost:9200/knowledge")
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
for i in range(len(db_objs)):
    es.index(index='knowledge', ignore=400, doc_type='document', id=i+1, body=db_objs[i])

print("done inserting documents")
