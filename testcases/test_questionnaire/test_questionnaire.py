import shelve
import pytest
import yaml
from Api.questionnaire.questionnaire import Questionnaire
from Api.utils import Util
from common.contants import test_questionnaire_dir, env_dir

def get_data(option):
    with open(test_questionnaire_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class TestQuestionnaire:

    _env = yaml.safe_load(open(env_dir, encoding="utf-8"))
    # 處理psd,根據環境變量獲取統一密碼
    _password = _env["password"][_env["default"]]

    def setup(self):
        '''
        創建數據庫保存返回數據resp
        '''
        self.db = shelve.open("resp")

    def teardown(self):
        '''
        關閉數據庫
        '''
        self.db.close()

    def token(self,username,password):
        return Util().token(username,password)

    def ques_t(self):
        return Questionnaire().questionnaire_t()

    def ques_s(self):
        return Questionnaire().questionnaire_s()

    @pytest.mark.parametrize("data",get_data("test_teacher_all"))
    def test_teacher_all(self,data):
        '''
        批量填写教师健康申报表
        '''
        try:
            assert True == self.token(data["username"], str(self._password))
            self.db["resp"] = self.ques_t()
            assert True == self.db["resp"]['success']
        except Exception as e:
            print(self.db["resp"]["errorMsg"])
            raise e

    @pytest.mark.parametrize("data",get_data("test_student_all"))
    def test_student_all(self,data):
        '''
        批量填写学生健康申报表
        '''
        try:
            assert True == self.token(data["username"], str(self._password))
            self.db["resp"] = self.ques_s()
            assert True == self.db["resp"]['success']
        except Exception as e:
            print(self.db["resp"]["errorMsg"])
            raise e


