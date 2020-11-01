# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import requests
import json


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "weixin"

            list = [token, timestamp, nonce]
            print("before sort: token, timestamp, nonce: ", list)
            list.sort()
            print("after sort: token, timestamp, nonce: ", list)
            sha1 = hashlib.sha1()
            # map(sha1.update, list)
            sha1.update("".join(list).encode('utf-8'))
            hashcode = sha1.hexdigest()
            print("hashcode: ", hashcode)
            print("data.signature, data.timestamp, data.nonce, data.echostr: ", data.signature, data.timestamp, data.nonce, data.echostr)
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except:
            return "error"

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # content = "test"
                # content = recMsg.Content.decode()
                content = get_rasa_reply(recMsg.Content.decode())
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print("return success")
                return "success"
        except:
            return "error"


def get_rasa_reply(user_input):
    print("user input: " + user_input)
    input_dict = {
        "message": user_input
    }
    panda_bot_data = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook', data=json.dumps(input_dict))
    panda_bot_data = panda_bot_data.text
    print("rasa reply: " + panda_bot_data)
    reply_info_list = json.loads(panda_bot_data)
    result_list = []
    for reply_info in reply_info_list:
        if "text" in reply_info:
            result_list.append(reply_info["text"])
        elif "image" in reply_info:
            result_list.append(reply_info["image"])
    print("final reply: " + ",".join(result_list))
    return "\n".join(result_list)


if __name__ == '__main__':
    print(get_rasa_reply("aaa"))

