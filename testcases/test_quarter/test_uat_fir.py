import datetime
import random
import shelve

import pytest
import yaml

from Api.quarter.quarter import My_Survey_Controller, Survey_Manage_Controller, Attachment_Controller
from Api.utils import Util
from common.contants import env_dir,test_uat_fir_dir


def get_data(option):
    with open(test_uat_fir_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class Test_Uat_Fir:

    _env = yaml.safe_load(open(env_dir, encoding="utf-8"))
    # 處理psd,根據環境變量獲取統一密碼
    _password = _env["password"][_env["default"]]
    # 獲取隨機數
    _num = str(random.randint(0,999))
    _date = datetime.datetime.now()
    # 獲取當前日期
    _now_date = datetime.datetime.now().strftime("%Y/%m/%d")
    # 獲取當前時間，多加2min
    _after_two_time = str((_date + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S"))
    # 獲取當前時間，減少1h
    _pre_five_time = str((_date - datetime.timedelta(hours=1)).strftime("%H:%M"))
    # 獲取當前日期，多加2天
    _after_two_date = str((_date + datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"))

    def token(self,username,password):
        return Util().token(username,password)

    def survey_manages(self,params=None):
        '''
        獲取問卷管理列表數據
        '''
        title_list = []
        datas = Survey_Manage_Controller().survey_manages(params)["data"]
        # for data in datas:
        #     title_list.append(data["title"])
        return datas

    def survey_manages_post(self,json,taskId=None):
        '''
        创建问卷
        '''
        # 处理json里的特殊数据
        if taskId:
            json["taskId"] = taskId
        if json["planExpireTime"] is  None:
            json["planExpireTime"] =self._after_two_date
        json["title"] = self._now_date + json["title"] + self._num
        json["startTime"] =self._after_two_time
        return Survey_Manage_Controller().survey_manages_post(json)

    def my_survey(self,params=None):
        '''
        獲取我的问卷列表數據
        '''
        title_list = []
        datas = My_Survey_Controller().my_survey(params)["data"]
        for data in datas:
            title_list.append(data["title"])
        return title_list

    def remove(self,id):
        '''
        刪除問卷
        '''
        return Survey_Manage_Controller().remove(id)

    @pytest.mark.parametrize("data", get_data("test_survey_manages_for_admin"))
    def test_survey_manages_for_admin(self, data):
        '''
        驗證創建問卷后，管理員能狗查看該問卷
        '''
        quarter = {}
        title_list = []
        db = shelve.open("quarter")
        if data["is_type"] == "create":
            # 創建問卷
            assert True == self.token(data["username"], str(self._password))
            assert data["expect"] == self.survey_manages_post(data["json"])["success"]
            datas = self.survey_manages()[0]
            quarter["title"] = datas["title"]
            quarter["id"]=datas["id"]
            db["quarter"] = quarter
        elif data["is_type"] == "search":
            # 驗證管理員有查看問卷的功能
            assert True == self.token(data["username"], str(self._password))
            resps = self.survey_manages()
            for resp in resps:
                title_list.append(resp["title"])
            if db["quarter"]["title"] in title_list:
                assert data["expect"] == True
            else:
                assert data["expect"] == False
        else:
            # 刪除問卷
            assert True == self.token(data["username"], str(self._password))
            assert True == self.remove(db["quarter"]["id"])["success"]
        db.close()

    # @pytest.mark.parametrize("data", get_data("test_my_survey"))
    # def test_my_survey(self, data):
    #     '''
    #     驗證
    #     '''
    #     assert True == self.token(data["username"], str(self._password))
    #     if data["title"] in self.my_survey():
    #         print(f"title:{data['title']}")
    #         assert data["expect"] == True
    #     else:
    #         assert data["expect"] == False
