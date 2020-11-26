import json
import requests
import datetime

import yaml


class BaseApi:
    params={}
    env = yaml.safe_load(open("../data/env.yaml"))

    def send(self,data):
        raw_data = json.dumps(data)
        for key, value in self.params.items():
            raw_data = raw_data.replace("${" + key + "}", value)
        data = json.loads(raw_data)
        # 處理url
        data["url"] = str(data["url"]). \
            replace("testing-studio", self.env["testing-studio"][self.env["default"]])
        print(f"查看請求參數：{data}")
        return requests.request(**data).json()


