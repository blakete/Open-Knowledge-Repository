
import sys
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(host='localhost', port=27017)
db=client.knowledge
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)
mycol = db["highlights"]
x = mycol.find_one()
print(x)

mycol.create_index([('text', 'text'), ('match', 'text'), ('title', 'text')])
cursor = mycol.find({"$text": {"$search": "hello mongo"}})

for doc in cursor:
    print(doc)

# import json
# from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
# db = client['knowledge']
# collection_currency = db['highlights']

# print(collection_currency)
# # cursor = collection_currency.find({})
# # for document in cursor:
# #     print(document)

# print("closing...")
client.close()