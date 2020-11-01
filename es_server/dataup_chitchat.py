#-*- coding:utf-8 -*- 
# Author: PX

import jieba
import json
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch import helpers


file_r = open("chitchat_panda.json", "r")
json_data = json.load(file_r)
keys = json_data.keys()
file_r.close()

es_hosts = ["127.0.0.1:9200"]
body = []
cnt = 0
for key in keys:
    seg_list = jieba.cut(key, cut_all=False)
    quest_sp = " ".join(seg_list)
    body.append({
        "_index": "chitchat_panda",
        "_type": "artice",
        "_id": cnt + 1,
        "_source": {
            "sp_quest": quest_sp,
            "quest": key,
            "q_type": "chat",
            "q_answer": json_data[key]
        }
    })
    cnt += 1

es = Elasticsearch(es_hosts)
helpers.bulk(es, body)
res = es.search(index='chitchat', body={"query": {"match_all": {}}})
pprint(res)

