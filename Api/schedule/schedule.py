import yaml
from Api.BaseApi import BaseApi
from common.contants import schedule_dir


class Schedele(BaseApi):

    with open(schedule_dir, encoding="utf-8") as f:
        data = yaml.load(f)

    def events(self,endTime,startTime):
         '''
         獲取教職員日曆頁的日程事件
         '''
         self.params["endTime"] = endTime
         self.params["startTime"] = startTime
         try:
            self._resp = self.send(self.data["events"],"schedule-url")
            return self._resp
         except Exception as e:
             print(f"events接口報錯!")
             raise e