# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import random
import socket
import requests
import time
import json
import http.client
from elasticsearch import Elasticsearch
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted, AllSlotsReset

es = Elasticsearch(["127.0.0.1:9200"])
weather_info_dict = {}


class SalesForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "sales_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "job_function",
            "use_case",
            "budget",
            "person_name",
            "company",
            "business_email",
        ]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message("谢谢您的咨询，我们稍后将和您联系！")
        return [AllSlotsReset()]


class WeatherForm(FormAction):
    def name(self):
        return "weather_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "weather_city",
            "weather_date"
        ]

    def get_html(self, url):
        """
        模拟浏览器来获取网页的html代码
        """
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webo,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
        }
        # 设定超时时间，取随机数是因为防止被网站认为是爬虫
        timeout = random.choice(range(80, 180))
        while True:
            try:
                rep = requests.get(url, headers=header, timeout=timeout)
                rep.encoding = "utf-8"
                break
            except socket.timeout as e:
                print("3:", e)
                time.sleep(random.choice(range(8, 15)))

            except socket.error as e:
                print("4:", e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e:
                print("5:", e)
                time.sleep(random.choice(range(30, 80)))

            except http.client.IncompleteRead as e:
                print("6:", e)
                time.sleep(random.choice(range(5, 15)))
        return rep.text

    def get_data(self, html_txt):
        weather_dict = json.loads(html_txt)
        new_dict = {}
        if weather_dict.get('desc') == 'OK':
            today = weather_dict.get('data').get('forecast')
            new_dict["城市"] = weather_dict.get('data').get('city') + '.'
            new_dict["温度"] = weather_dict.get('data').get('wendu') + '℃'
            new_dict["最高温"] = today[0].get('high').replace('高温', '') + '.'
            new_dict["最低温"] = today[0].get('low').replace('低温', '') + '.'
            new_dict["天气"] = today[0].get('type')
            new_dict["status"] = weather_dict["status"]
            return new_dict

    def get_url(self, city_name):
        weather_url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city_name
        return weather_url

    def get_res(self, location):
        if location in weather_info_dict:
            return weather_info_dict[location]
        url = self.get_url(location)
        html = self.get_html(url)
        new_dict = self.get_data(html)
        result = requests.get(
            "https://api.seniverse.com/v3/weather/daily.json?key=SCZkY8YxwznTuManP&location=重庆&language=zh-Hans&unit=c&start=-1&days=16")
        d = json.loads(result.text)
        print(json.dumps(d, ensure_ascii=False, indent=2))
        print("天数: %d" % len(d["results"][0]["daily"]))
        print("result code: %d" % result.status_code)
        if result.status_code == 200:
            daily_info_list = json.loads(result.text)["results"][0]["daily"]

            # 已经很晚了，为你预报明天天气，北京明天多云转晴，22度至34度，比今天热一点，空气质量指数39，空气很好（不错），天气热，多喝水防上火。
            print("【地点】【日期】【白天天气现象】转【晚上天气现象】，【最低温度】至【最高温度】")
            print()
        else:
            return ''

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        user_entities = tracker.latest_message.get('entities')
        user_province = ''
        user_city = ''
        for value in user_entities:
            if value['entity'] == 'province':
                user_province = value['value']
            if value['entity'] == 'city':
                user_city = value['value']
        province_city_dict = dict()
        with open('data/province_city') as f:
            province_city_dict = json.load(f)
        provinces = province_city_dict.keys()
        if len(user_city) == 0 and len(user_province) != 0:
            # if '省' in user_province and user_province in provinces:
            #   user_city=province_city_dict[user_province][0]
            # if user_province+'省' in provinces:
            #    user_city= province_city_dict[user_province+'省'][0]
            for p in provinces:
                if user_province in p:
                    user_city = province_city_dict[p][0]
                    break
        elif len(user_city) != 0:
            for p in provinces:
                if user_city in p:
                    user_city = province_city_dict[p][0]
                    break
        elif len(user_city) == 0 and len(user_province) == 0:
            user_city = "北京"
        try:
            res = self.get_res(user_city)
        except:
            res = "请输入正确的地名"
        dispatcher.utter_message(res)
        return [AllSlotsReset()]


# 闲聊
class ActionChitchat(Action):
    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        confirm_meaasge = ["嗯嗯", "嗯呢", "哦了", "噢了", "欧了", "没问题", "没毛病", "可以", "ok", "OK", "Ok", "oK"]
        msg_chitchat = tracker.latest_message.get("text")
        if msg_chitchat.strip() in confirm_meaasge and tracker.current_slot_values() is not None:
            dispatcher.utter_message("小熊已经帮您搞定了")
            return [AllSlotsReset()]
        else:
            results_chitchat = es.search(index='chitchat_panda',
                            body={"query": {"match": {"quest": msg_chitchat}}})
            if results_chitchat["hits"]["max_score"] is None:
                dispatcher.utter_message("小熊正在不断成长中,您可以换个问题")
                return [UserUtteranceReverted()]
            else:
                answer = results_chitchat["hits"]["hits"][0]["_source"]["q_answer"]
                if type(answer) == list:
                    answer = random.choice(answer)
                dispatcher.utter_message(str(answer))
                return [UserUtteranceReverted()]
