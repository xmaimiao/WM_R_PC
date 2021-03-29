import datetime

import pytest
import yaml
from pytest_check import check

from Api.class_timetable.class_timetable import Call_Roll_Controller, Lesson_Controller, Sign_Record_Controller, \
    Setting_Controller, Classdata_Controller, Sign_Statistics_Controller
from Api.utils import Util
from common.contants import env_dir, test_class_timetable_dir


def get_data(option):
    with open(test_class_timetable_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas


class Test_Class_Timetable:
    _env = yaml.safe_load(open(env_dir, encoding="utf-8"))
    # 處理psd,根據環境變量獲取統一密碼
    _password = _env["password"][_env["default"]]

    _date = datetime.datetime.now()
    # 獲取當前时间
    _now_time = datetime.datetime.now().strftime("%H:%M:%S")
    # 獲取當前時間，多加1min
    _after_one_time = str((_date + datetime.timedelta(minutes=1)).strftime("%H:%M:%S"))

    def token(self, username, password):
        return Util().token(username, password)

    # 点名接口
    def change_room(self, json):
        '''
        切换教室(多个lessonId)
        '''
        return Call_Roll_Controller().change_room(json)

    def lessons_recent(self, params):
        '''
        查詢指定班別下當前點名(id為-1，表示沒有點名)
        '''
        return Call_Roll_Controller().lessons_recent(params)

    def teacher_lessons(self, json):
        '''
        老師發起點名(多个lessonId)
        '''
        return Call_Roll_Controller().teacher_lessons(json)

    # 课表接口
    def recent(self):
        '''
        獲取教師當前或最近的一門課，可獲取課程id，班級id，最新的點名學生簽到id
        '''
        return Lesson_Controller().recent()

    def lessons_student_now_sync(self):
         '''
         我的课表（学生端）- 刷新
         '''
         return Lesson_Controller().lessons_student_now_sync()

    # 班别接口
    def classdatas_deg_course_managers(self):
        '''
        獲取教師當前或最近的一門課，可獲取課程id，班級id，最新的點名學生簽到id
        '''
        return Classdata_Controller().classdatas_deg_course_managers()

    # 签到统计接口
    def sign_statistics_degrees_students(self,params):
        '''
        獲取教師當前或最近的一門課，可獲取課程id，班級id，最新的點名學生簽到id
        '''
        return Sign_Statistics_Controller().sign_statistics_degrees_students(params)

    def sign_statistics_degrees_resign_absent(self,json):
        '''
        補簽或缺席(本科生)
        '''
        return Sign_Statistics_Controller().sign_statistics_degrees_resign_absent(json)

    # 签到记录接口
    def sign_records_users(self):
        '''
        查詢用戶當前是否有簽到記錄。課表為-1時，表示沒有簽到記錄
        '''
        return Sign_Record_Controller().sign_records_users()

    def sign(self, json, signid):
        '''
        用戶簽到(uuid、major、minor 從打卡項目中獲得)
        '''
        return Sign_Record_Controller().sign(json, signid)

    def sign_records_lessons(self, params):
        '''
        查询多节课下的签到记录 :獲取用戶簽到id、用户签到状态用
        '''
        return Sign_Record_Controller().sign_records_lessons(params)

    def resign_mobiles(self, json):
        '''
        查询多节课下的签到记录 :獲取用戶簽到id用
        '''
        return Sign_Record_Controller().resign_mobiles(json)

    # 设置接口
    def settings(self):
        '''
        获取设置列表
        '''
        return Setting_Controller().settings()

    #     测试用例部分

    # def setup(self):
    #     assert True == self.token("pyyan", str(self._password))

    @pytest.mark.parametrize("data", get_data("test_change_room"))
    def test_change_room(self, data):
        '''
        测试切换教室
        '''
        assert True == self.token(data["username"], str(self._password))
        json = data["json"]
        json["lessonIds"] = [self.recent()["model"]["id"], ]
        resp = self.change_room(json)
        assert True == resp['success']

    @pytest.mark.parametrize("data", get_data("test_teacher_lesson"))
    def test_teacher_lesson(self, data):
        '''
        测试老师发起点名
        '''
        assert True == self.token(data["username"], str(self._password))
        lessonid = self.recent()["model"]["id"]
        json = {"lessonIds": [lessonid, ]}
        # 获取教师最近一节课的id，判断是否在点名中
        condition = self.lessons_recent({"lessonIds": lessonid})["model"]["id"]
        if condition == -1:
            resp = self.teacher_lessons(json)
            assert True == resp['success']
        else:
            print("当前正在点名中！")
            assert True == False

    @pytest.mark.parametrize("data", get_data("test_student_sign"))
    def test_student_sign(self, data):
        '''
        测试学生签到
        '''
        assert True == self.token(data["username"], str(self._password))
        signid = self.sign_records_users()["model"]["id"]
        if signid != '-1':
            resp = self.sign(data["json"], signid)
            assert True == resp['success']
        else:
            print("签到id为-1，学生不可签到！")
            assert True == False

    @pytest.mark.parametrize("data", get_data("test_student_sign_late"))
    def test_student_sign_late(self, data):
        '''
        测试学生首次签到-》迟到
        '''
        assert True == self.token(data["t_username"], str(self._password))
        # 获取上课N分钟后签到-》迟到
        late_settings = self.settings()["model"][-1]["value"]
        late_settings = int(late_settings) + 1
        assert True == self.token(data["s_username"], str(self._password))
        model = self.sign_records_users()["model"]
        # 获取学生签到id
        signid = model["id"]
        try:
            # 获取课程上课开始时间
            lessonStartTime = model["lessonVO"]["lessonStartTime"]
            # 获取当前时间
            timenow = datetime.datetime.now()
            # 计算从该时间点签到算迟到
            late_time = (timenow - datetime.timedelta(minutes=late_settings)).strftime('%H:%M')
            if signid != '-1' and late_time >= lessonStartTime:
                resp = self.sign(data["json"], signid)
                assert True == resp['success']
            else:
                print("该学生签到id为-1！")
                assert True == False
        except Exception as e:
            print("该学生签到id为-1!")
            raise e

    @pytest.mark.parametrize("data", get_data("test_app_resign"))
    def test_app_resign(self, data):
        '''
        測試從app進行補簽
        '''
        # 获取教师token
        assert True == self.token(data["username"], str(self._password))
        params = data["params"]
        # 获取课程id
        params["lessonIds"] = self.recent()["model"]["id"]
        # 獲取第N次點名的學生簽到id
        model = self.sign_records_lessons(params)["model"]
        signid_list = []
        for sign_s in model:
            if sign_s["studentNo"] in data["studentNo_list"]:
                signid_list.append(sign_s["id"])
        resign_json = data["resign_json"]
        resign_json["ids"] = signid_list
        # 补签
        resp = self.resign_mobiles(resign_json)
        assert True == resp['success']
        # 验证学生已补签成功
        model = self.sign_records_lessons(params)["model"]
        for sign_s in model:
            if sign_s["studentNo"] in data["studentNo_list"]:
                assert sign_s["status"] == "RESIGN"


    @pytest.mark.parametrize("data", get_data("test_statistics_degrees"))
    def test_statistics_degrees(self, data,check,params = None):
        '''
        PC端查询学生签到记录：签到状态
        '''
        if params == None:
            params = data["params"]
        assert True == self.token(data["username"], str(self._password))
        sign_data = self.sign_statistics_degrees_students(params)["data"]
        check.not_equal(sign_data, [], "sign_data为空，暂无签到记录！")
        lessonDate_signdate= {}
        for user_record in sign_data:
            if user_record["studentNo"] in data["stu_dict"]:
                studentNo = user_record["studentNo"]
                for signdate in user_record["signDateVOList"]:
                    if signdate["lessonDate"] == data["lessondate"]:
                        lessonDate_signdate[f"{studentNo}"] = signdate["status"]
        diff = lessonDate_signdate.keys() & data["stu_dict"]
        diff_vals = [(k, lessonDate_signdate[k], data["stu_dict"][k]) for k in diff if lessonDate_signdate[k] != data["stu_dict"][k]]
        diff_tuple = data["stu_dict"].keys() - lessonDate_signdate.keys()
        assert lessonDate_signdate != {},f"{data['lessondate']}的簽到記錄不存在"
        assert diff_vals == [],"測試數據實際結果與預期結果不一致"
        assert diff_tuple == set(), f"測試學號{diff_tuple}找不到簽到記錄"

    # @pytest.mark.parametrize("data", get_data("test_degrees_resign_absent"))
    # def test_degrees_resign(self,data):
    #     '''
    #     补签本科生）
    #     '''
    #     assert True == self.token(data["username"], str(self._password))
    #     if data["operate"]


    @pytest.mark.parametrize("data", get_data("test_check_exam"))
    def test_check_exam(self, data):
        '''
        验证考试存在
        '''
        assert True == self.token(data["s_username"], str(self._password))
        resp = self.lessons_student_now_sync()
        assert True == resp['success']




