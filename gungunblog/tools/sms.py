import base64
import datetime
import hashlib
import json

import requests


class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    def get_request_url(self, sig):
        self.url = self.base_url + f'/2013-12-26/Accounts/{self.accountSid}/SMS/TemplateSMS?sig={sig}'
        return self.url

    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self, timestamp):
        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_request_header(self, timstamp):
        s = self.accountSid + ":" + timstamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Content-Length':'',
            'Authorization': auth
        }

    def get_request_body(self, phone, code):
        return {
            "to": phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, '5']
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)
        print(url)
        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        data = self.request_api(url, header, json.dumps(body))
        return data


if __name__ == '__main__':
    config = {
        "accountSid": '8aaf07087b9a3d03017ba0580a97014f',
        "accountToken": '6728df5319e24808a73c5dbb6dd0c7eb',
        "appId" : '8aaf07087b9a3d03017ba0580b880155',
        "templateId": '1'
    }
    yun = YunTongXin(**config)
    res = yun.run('15727890575', '970810')
    print(res)
# {"statusCode":"000000","templateSMS":{"smsMessageSid":"5b31cf7c34fb42f6b3130dba8f6daf6d","dateCreated":"20210901215409"}}