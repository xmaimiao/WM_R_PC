import pytest
import yaml

from Api.questionnaire.questionnaire import Questionnaire
from Api.utils import Util

def get_data(option):
    with open("../data/test_questionnaire.yaml") as f:
        datas = yaml.safe_load(f)[option]
        return datas

class TestQuestionnaire:

    _env = yaml.safe_load(open("../data/env.yaml"))
    # 處理psd,根據環境變量獲取統一密碼
    _password = _env["password"][_env["default"]]
    print(_password)

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
        :param data:
        :return:
        '''
        assert True == self.token(data["username"],str(self._password))
        try:
            assert True == self.ques_t()['success']
        except Exception as e:
            print(self.ques_t()['errorMsg'])
            raise e

    @pytest.mark.parametrize("data",get_data("test_student_all"))
    def test_student_all(self,data):
        '''
        批量填写学生健康申报表
        :param data:
        :return:
        '''
        assert True == self.token(data["username"],str(self._password))
        try:
            assert True == self.ques_s()['success']
        except Exception as e:
            print("今日已提交過")
            raise e


