import yaml
from Api.BaseApi import BaseApi
from common.contants import quarter_dir

def get_data(option):
    with open(quarter_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class Survey_Manage_Controller(BaseApi):
    '''问卷管理'''

    def survey_manages(self,params=None):
         '''
         獲取問卷管理列表數據
         '''
         data = get_data("survey_manages")
         if params:
             data["params"] = params
         try:
            self.resp = self.send(data,"quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
         except Exception as e:
             print(f"survey_manages接口報錯!")
             raise e

    def survey_manages_post(self,json):
        '''
        創建問卷
        '''
        data = get_data("survey_manages_post")
        data["json"] = json
        try:
            self.resp = self.send(data=data, api_name="quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
        except Exception as e:
            print(f"survey_manages_post接口報錯!")
            raise e

    def remove(self,id):
        '''
        刪除問卷
        '''
        self.params["id"] = id
        try:
            self.resp = self.send(get_data("remove"),"quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
        except Exception as e:
            print(f"remove接口報錯!")
            raise e

class My_Survey_Controller(BaseApi):
    def my_survey(self,params=None):
         '''
         獲取問卷管理列表數據
         '''
         data = get_data("my_survey")
         if params:
             data["params"] = params
         try:
            self.resp = self.send(data,"quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
         except Exception as e:
             print(f"my_survey接口報錯!")
             raise e

    def my_survey_submit(self,json=None):
         '''
         提交问卷
         '''
         data = get_data("my_survey_submit")
         if json:
             data["json"] = json
         try:
            self.resp = self.send(data,"quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
         except Exception as e:
             print(f"my_survey接口報錯!")
             raise e


class Attachment_Controller(BaseApi):
    def import_outsider(self, file):
        '''
        导入外部人員
        '''
        data = get_data("my_survey")
        data["file"] = file
        try:
            self.resp = self.send(data, "quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp["model"]
        except Exception as e:
            print(f"import_outsider接口報錯!")
            raise e

class Survey_Statistics_Controller(BaseApi):
    '''問卷統計'''
    def survey_statistics(self,params=None):
         '''
         獲取問卷統計列表數據
         '''
         data = get_data("survey_statistics")
         if params:
             data["params"] = params
         try:
            self.resp = self.send(data,"quarter-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
         except Exception as e:
             print(f"survey_statistics接口報錯!")
             raise e

