import pytest
import yaml
from Api.schedule.schedule import Schedele
from Api.utils import Util
from common.contants import test_schedule_dir, env_dir


def get_data(option):
    with open(test_schedule_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class Test_Schedule:

    _env = yaml.safe_load(open(env_dir, encoding="utf-8"))
    # 處理psd,根據環境變量獲取統一密碼
    _password = _env["password"][_env["default"]]
    global _resp

    def token(self,username,password):
        return Util().token(username,password)

    def events(self,date):
        title_list = []
        date_events = Schedele().events(endTime=date,startTime=date)["model"]
        for events in date_events:
            if date == events["date"]:
                for event in events["events"]:
                    if event["subType"] == "HR_NOTICE":
                        title = event["title"]
                        title_list.append(title)
        return title_list


    @pytest.mark.parametrize("data",get_data("test_teacher_events"))
    def test_teacher_events(self,data):
        '''
        獲取教職員日曆頁面的日程事件
        '''
        assert True == self.token(data["username"], str(self._password))
        if data["title"] in self.events(data["date"]):
            assert data["expect"] == True
        else:
            assert data["expect"] == False



