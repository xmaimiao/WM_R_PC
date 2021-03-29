import yaml
from Api.BaseApi import BaseApi
from common.contants import class_timetable_dir


def get_data(option):
    with open(class_timetable_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class Call_Roll_Controller(BaseApi):
    '''点名'''

    def change_room(self,json):
         '''
         切换教室(多个lessonId)
         '''
         try:
             data = get_data("change_room")
             data["json"] = json
             self.resp = self.send(data,"class-timetable-url")
             return self.resp
         except Exception as e:
             print(f"change_room接口報錯!")
             raise e

    def lessons_recent(self,params):
         '''
         查詢指定班別下當前點名(id為-1，表示沒有點名)
         '''
         try:
             data = get_data("lessons_recent")
             data["params"] = params
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"lessons_recent接口報錯!")
             raise e

    def teacher_lessons(self,json):
         '''
         老師發起點名(多个lessonId)
         '''
         try:
             data = get_data("teacher_lessons")
             data["json"] = json
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"teacher_lessons接口報錯!")
             raise e

class Lesson_Controller(BaseApi):
    '''课表'''

    def recent(self):
         '''
         獲取教師當前或最近的一門課
         '''
         try:
             self.resp = self.send(get_data("recent"),"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"recent接口報錯!")
             raise e

    def lessons_student_now_sync(self):
         '''
         我的课表（学生端）- 刷新
         '''
         try:
             self.resp = self.send(get_data("lessons_student_now_sync"),"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"lessons_student_now_sync接口報錯!")
             raise e

class Classdata_Controller(BaseApi):
    '''班别'''

    def classdatas_deg_course_managers(self):
         '''
         本科生-学期科目列表（管理端）
         '''
         try:
             self.resp = self.send(get_data("classdatas_deg_course_managers"),"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"classdatas_deg_course_managers接口報錯!")
             raise e

class Sign_Statistics_Controller(BaseApi):
    '''
    签到统计
    '''

    def sign_statistics_degrees_students(self,params):
         '''
         查询学生签到统计(本科生)
         '''
         data = get_data("sign_statistics_degrees_students")
         data["params"] = params
         try:
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"sign_statistics_degrees_students接口報錯!")
             raise e

    def sign_statistics_degrees_resign_absent(self,json):
        '''
        補簽或缺席(本科生)
        '''
        data = get_data("sign_statistics_degrees_resign_absent")
        data["json"] = json
        try:
            self.resp = self.send(data, "class-timetable-url")
            # print(f"self.resp:{self.resp}")
            return self.resp
        except Exception as e:
            print(f"sign_statistics_degrees_resign_absent接口報錯!")
            raise e

class Sign_Record_Controller(BaseApi):
    '''签到记录'''

    def sign_records_users(self):
         '''
         查詢用戶當前是否有簽到記錄。課表為-1時，表示沒有簽到記錄
         '''
         try:
             self.resp = self.send(get_data("sign_records_users"),"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"sign_records_users接口報錯!")
             raise e

    def sign(self,json,signid):
         '''
         用戶簽到(uuid、major、minor 從打卡項目中獲得)
         '''
         self.params["id"] = signid
         data = get_data("sign")
         data["json"] = json
         try:
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"sign接口報錯!")
             raise e

    def sign_records_lessons(self,params):
         '''
         查询多节课下的签到记录 :獲取用戶簽到id用
         '''
         data = get_data("sign_records_lessons")
         data["params"] = params
         try:
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"sign_records_lessons接口報錯!")
             raise e

    def resign_mobiles(self,json):
         '''
         查询多节课下的签到记录 :獲取用戶簽到id用
         '''
         data = get_data("resign_mobiles")
         data["json"] = json
         try:
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"resign_mobiles接口報錯!")
             raise e

class Setting_Controller(BaseApi):
    '''设置'''

    def settings(self):
         '''
         获取设置列表
         '''
         try:
             self.resp = self.send(get_data("settings"),"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"settings接口報錯!")
             raise e

    def settings_post(self,json):
         '''
         修改设置列表
         '''
         data = get_data("sign")
         data["json"] = json
         try:
             self.resp = self.send(data,"class-timetable-url")
             # print(f"self.resp:{self.resp}")
             return self.resp
         except Exception as e:
             print(f"settings_post接口報錯!")
             raise e