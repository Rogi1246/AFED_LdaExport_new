# importing the stuff needed
# import csv, json
import sys
import json
import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch

# first : an Elasticsearch instance is required
elastic_client = Elasticsearch(['betaweb015', 'betaweb017', 'betaweb020'],
                         sniff_on_start=True, sniff_on_connection_fail=True, timeout=360)

# toal num of documents to be retrieved :
total_docs = 20
# print("\n calling Elasticsearch for", total_docs, "docs ")
# API-call to the cluster to actually get docs

# "must": [{
#                 "match": {"text_plain": "pollution"}
#             }, {
#                 "match": {"text_plain": "waste"}
#             }]

query = {
    # "size": 10000,
    "_source": ["@timestamp","headers","text_plain"],
    "query": {
        "bool": {
            "must": [{
                "match": {"text_plain": "islam"}
            }]
        }
    }
}

# for certain number of docs
result = elastic_client.search(index='gmane*', body=query, size=total_docs)

# should be 20000 now
# result = elastic_client.search(index='gmane*', body=query, scroll='1m')
# scroll = result['_scroll_id']
# result2 = elastic_client.scroll(scroll_id=scroll, scroll='1m')

print(" putting them in a list ")
elastic_docs = result["hits"]["hits"]

# create empty Pandas Dataframe
docs = pd.DataFrame()

# iterate Es-docs in list
print("\n creating objects from data ")
for num, doc in enumerate(elastic_docs):
    # getting _source data
    source_data = doc["_source"]

    # getting _id
    _id = doc["_id"]

    # create series-object
    doc_data = pd.Series(source_data, name=_id)

    # append to DataFrame object
    docs = docs.append(doc_data)

print("\n exporting objects ")
# epxort as json file
docs.to_json("export_TEST.json")

# return JSON string of docs
json_export = docs.to_json()
# print("\n json data : ", json_export)


# let's start
# extract the headers and timestamps from the mails

test_data = open('export_TEST.json')
dataT = json.load(test_data)

# or just :
dtest = pd.read_json('export_TEST.json')

# printing headers and timestamps working.
print("---------------printing headers---------------")
print(dataT['headers'])
print("---------------printing timestamps---------------")
print(dataT['@timestamp'])

var = 'from' in dataT
print(var)
var2 = dataT.get('from')
print(var2)

test_data.close()
