# serve.py
import json
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == 'POST':
        # accept posted json object with search parameters
        req_data = request.get_json()
        search_terms = req_data["search"]
        print(f"Submitted search terms: {search_terms}")
        URL = "http://localhost:9200/knowledge/document/_search"
        search_string = "elasticsearch"
        PARAMS = {"query": {"multi_match" : {"query":search_terms, "fields": [ "text", "match" ]}}}
        r = requests.get(url = URL, json = PARAMS) 
        data = r.json() 
        # get all unique URLs from returned objects
        results = data['hits']['hits']
        urls = []
        for res in results:
            if res['_source']['url'] not in urls:
                urls.append(res['_source']['url'])

        # construct template json objects from all highlight documents of same url
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
                    # check for HTML and escape it
                    if bool(BeautifulSoup(res["_source"]["text"], "html.parser").find()):
                        newTxt = res["_source"]["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        res["_source"]["text"] = newTxt
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
        return json.dumps(templates)
    else:
        # TODO accept HTTP GET request and return generated web page like Google
        search_terms = language = request.args.get('search')
        print(f"Submitted search terms: {search_terms}")
        return json.dumps(resp)


if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')


