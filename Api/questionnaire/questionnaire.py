import yaml
from Api.BaseApi import BaseApi
from common.contants import questionnaire_dir


class Questionnaire(BaseApi):

    def __init__(self):
         with open(questionnaire_dir, encoding="utf-8") as f:
              self.data = yaml.load(f)

    def questionnaire_t(self):
         '''
         填寫教師健康申報表
         '''
         try:
            print(self.data["questionnaire_t"])
            self._resp = self.send(self.data["questionnaire_t"],"questionnaire-url")
            return self._resp
         except Exception as e:
            print(f"questionnaire接口報錯!")
            raise e

    def questionnaire_s(self):
         '''
         填寫學生健康申報表
         '''
         try:
             self._resp = self.send(self.data["questionnaire_s"],"questionnaire-url")
             return self._resp
         except Exception as e:
             print("questionnaire接口報錯!")
             raise e
