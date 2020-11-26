import os

import yaml
from Api.BaseApi import BaseApi


class Util(BaseApi):
    with open("../data/utils.yaml", encoding="utf-8") as f:
        data = yaml.load(f)["token"]

    def token(self,username,password):
        '''
        獲取token
        '''
        self.params["username"] = username
        self.params["password"] = password
        # 處理token
        self.data["url"] = str(self.data["url"]). \
            replace("token-testing-studio", self.env["token-testing-studio"][self.env["default"]])
        # 處理Authorization
        self.data["headers"]["Authorization"] = str(self.data["headers"]["Authorization"]). \
            replace("Authorization-testing-studio", self.env["Authorization-testing-studio"][self.env["default"]])
        resp = self.send(self.data)
        token = self.params["token"] = resp['model']['accessToken']
        print(f"查看啊token：{token}")
        return resp['success']
