import json
import pandas

from elasticsearch import Elasticsearch

# Elasticsearch instance required
elastic_client = Elasticsearch(['betaweb015', 'betaweb017', 'betaweb020'],
                         sniff_on_start=True, sniff_on_connection_fail=True, timeout=360)

# toal num of documents to be retrieved :
total_docs = 2
# API-call to the cluster to actually get docs
# query
query = {
    # "size": 10000,
    "_source": ["main_content"],
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
# scroll API needed
# result = elastic_client.search(index='gmane*', body=query, scroll='1m')
# scroll = result['_scroll_id']
# result2 = elastic_client.scroll(scroll_id=scroll, scroll='1m')

print(" putting them in a list ")
elastic_docs = result["hits"]["hits"]

# create empty Pandas Dataframe
docs = pandas.DataFrame()

# iterate Es-docs in list
print("\n creating objects from data ")
for num, doc in enumerate(elastic_docs):
    # getting _source data
    source_data = doc["_source"]

    # getting _id
    _id = doc["_id"]

    # create series-object
    doc_data = pandas.Series(source_data, name=_id)

    # append to DataFrame object
    docs = docs.append(doc_data)

print("\n exporting objects ")
# export as json file
docs.to_json("export_mainContent.json")

# return JSON string of docs
json_export = docs.to_json()
# print("\n json data : ", json_export)
