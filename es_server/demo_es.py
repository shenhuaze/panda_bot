
import json
import sys
from elasticsearch import Elasticsearch


if __name__ == '__main__':
    # 用法: python demo_es.py 讲个笑话
    es = Elasticsearch(["127.0.0.1:9200"])
    text = "你是谁开发的"
    if len(sys.argv) > 1:
        text = sys.argv[1]
    print("输入：%s" % text)
    results = es.search(index='chitchat_panda', body={"query": {"match": {"quest": text}}})
    # print("所有查询结果：%s")
    # print(json.dumps(results, ensure_ascii=False, indent=2))
    if results["hits"]["max_score"] is None:
        print("输出：没找到答案！！！")
    else:
        answer = results["hits"]["hits"][0]["_source"]["q_answer"]
        print("输出：" + str(answer))
