# import pytest
#
#
# @pytest.fixture(scope='module')
# def login():
#     print("登录方法")
#     # 相当于return
#     yield 2
#     print("退出方法")
#     return 3
#
#
# def test_case1(login):
#     print(f"case1 login={login}")
#
#
# def test_case2():
#     print("case2")




def test_data():
    list1 = ['张三', '李四', '老二']
    # 数据库返回值

    list2 = ['张三', '李四', '老二', '王七']

    c = [x for x in list1 if x not in list2]  #在list1列表中而不在list2列表中

    print(c)

