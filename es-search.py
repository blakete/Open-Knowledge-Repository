import json
import requests 
URL = "http://localhost:9200/knowledge/document/_search"
search_string = "elasticsearch"
PARAMS = {"query": {"multi_match" : {"query":search_string, "fields": [ "text", "match" ]}}}
r = requests.get(url = URL, json = PARAMS) 
data = r.json() 
# get all unique URLs from returned objects
results = data['hits']['hits']
urls = []
for res in results:
    if res['_source']['url'] not in urls:
        urls.append(res['_source']['url'])

# TODO construct template json objects from all highlight documents of same url
template = {
    "red":[],
    "yellow":[],
    "cyan":[],
    "url":None
}
templates = []
for url in urls:
    curr_temp = {
        "red":[],
        "yellow":[],
        "cyan":[],
        "url":None
    }
    curr_temp['url'] = url
    PARAMS = {"query":{"match": {"url": {"query": url}}}}
    r = requests.get(url = URL, json = PARAMS) 
    data = r.json()
    results = data['hits']['hits']
    # print(f"matching: {url}")
    for res in results:
        # confirms exact match with url
        if res["_source"]["url"] == url:
            # print(res["_source"]["url"])
            res["_source"].pop("verb", None)
            res["_source"].pop("highlight_id", None)
            res["_source"].pop("url", None)
            if res["_source"]["className"] == "red":
                curr_temp["red"].append(res["_source"])
            elif res["_source"]["className"] == "yellow":
                curr_temp["yellow"].append(res["_source"])
            elif res["_source"]["className"] == "cyan":
                curr_temp["cyan"].append(res["_source"])
    templates.append(curr_temp.copy())

print(json.dumps(templates))




# {
#     "red":[
#         {
#         "timestamp":1595014017335,
#         "value":"Open-Knowledge-Repository (OKR)",
#         "color":"red"
#         }
#     ],
#     "yellow":[
#         {
#         "timestamp":1595014017338,
#         "value":"Open source tool to share knowledge across teams.",
#         "color":"yellow"
#         },
#         {
#         "timestamp":1595014017338,
#         "value":"Download the respository from github:",
#         "color":"yellow"
#         }
#     ],
#     "cyan":[
#         {
#         "timestamp":1595014017339,
#         "value":"git clone git@github.com:blakete/Open-Knowledge-Repository.git",
#         "color":"blue"
#         }
#     ],
#     "src":"https://google.com"
# }

