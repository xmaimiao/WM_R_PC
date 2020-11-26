import yaml

from Api.BaseApi import BaseApi


class Questionnaire(BaseApi):

    def __init__(self):
         with open(".././data/questionnaire.yaml", encoding="utf-8") as f:
              self.data = yaml.load(f)

    def questionnaire_s(self):
         '''
         填寫學生健康申報表
         :return:
         url:https://api.must.edu.mo/classtimetable-coes
         :return:
         '''
         resp = self.send(self.data["questionnaire_s"])
         return resp

    def questionnaire_t(self):
         '''
         填寫教師健康申報表
         '''
         resp = self.send(self.data["questionnaire_t"])
         return resp