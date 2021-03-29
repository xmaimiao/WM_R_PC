import json
import requests
import yaml

from common.contants import env_dir


class BaseApi:
    params={}
    with open(env_dir, encoding="utf-8") as f:
        env = yaml.load(f)

    def send(self,data,api_name=None):
        raw_data = json.dumps(data)
        for key, value in self.params.items():
            raw_data = raw_data.replace("${" + key + "}", str(value))
        data = json.loads(raw_data)
        # 處理url
        if api_name:
            data["url"] = str(data["url"]). \
                replace(api_name, self.env[api_name][self.env["default"]])
        print(f"查看請求參數：{data}")
        return requests.request(**data).json()


