# @author Huaze Shen
# @date 2019-12-10

import requests
import json

info_dict = {
    # "sender": "Rasa",
    "message": "不好"
}

panda_bot_data = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook', data=json.dumps(info_dict))
panda_bot_data = panda_bot_data.text
panda_bot_data = json.loads(panda_bot_data)
print(panda_bot_data)
for line in panda_bot_data:
    print(line)
