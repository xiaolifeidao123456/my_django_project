import json

from django.contrib.sites import requests


class Message:

    def __init__(self, api_key):
        # 960570162a9467f48111c8adde5efd65
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'api_key': self.api_key,
            'mobile': mobile,
            'text': '【乐搜网】您的手机验证码是{code}。本条信息无需回复'.format(code=code)
        }
        response = requests.post(self.single_send_url, params)
        result = json.loads(response.text)
        print(result)

msg = Message('960570162a9467f48111c8adde5efd65')
