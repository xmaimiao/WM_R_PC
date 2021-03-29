import datetime
import random

import pytest
import yaml

from Api.quarter.quarter import My_Survey_Controller, Survey_Manage_Controller, Attachment_Controller, \
    Survey_Statistics_Controller
from Api.utils import Util
from common.contants import env_dir, test_prod_dir


def get_data(option):
    with open(test_prod_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class Test_Quarter:

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
    # 獲取當前時間，多加4min
    _after_four_time = str((_date + datetime.timedelta(minutes=4)).strftime("%Y-%m-%d %H:%M:%S"))
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
        return Survey_Manage_Controller().survey_manages(params)

    def survey_manages_post(self,json,taskId=None,startTime=None,planExpireTime=None):
        '''
        创建问卷
        '''
        # 处理json里的特殊数据
        if taskId:
            json["taskId"] = taskId
        if json["planExpireTime"] is  None:
            json["planExpireTime"] = planExpireTime
        if json["startTime"] is  None:
            json["startTime"] =startTime
        json["title"] = self._now_date + json["title"] + self._num
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

    def import_outsider(self,file_path):
        '''
        获取外部人员的id
        '''
        file_data = {'file': (open(file_path, 'rb'),'application/json')}
        return Attachment_Controller().import_outsider(file_data)["model"]

    def remove(self,id):
        '''
        刪除問卷
        '''
        return Survey_Manage_Controller().remove(id)

    def survey_statistics(self,params=None):
        '''
        獲取問卷統計列表數據
        '''
        return Survey_Statistics_Controller().survey_statistics(params)


    @pytest.mark.parametrize("data",get_data("test_survey_manages_post"))
    def test_survey_manages_post(self,data):
        '''
        创建问卷
        '''
        assert True == self.token(data["username"], str(self._password))
        assert data["expect"] == self.survey_manages_post(data["json"],startTime=self._after_two_time,planExpireTime=self._after_four_time)["success"]
