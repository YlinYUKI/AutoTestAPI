import requests
from common.handle_conf import conf
from jsonpath import jsonpath
class BaseTest:
    @classmethod
    def admin_login(cls):
        # ----------------------管理员登录-------------------------------
        url = conf.get('env', 'base_url') + '/member/login'
        headers = eval(conf.get('env', 'headers'))
        params = {
            "mobile_phone": conf.get('test_data', 'admin_mobile'),
            "pwd": conf.get('test_data', 'admin_pwd')
        }
        response = requests.post(url=url, headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers["Authorization"] = "Bearer " + token
        id = jsonpath(res, '$..id')[0]
        cls.admin_member_id = id
        cls.admin_headers = headers

    @classmethod
    def user_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        headers = eval(conf.get('env', 'headers'))
        params = {
            "mobile_phone": conf.get('test_data', 'mobile'),
            "pwd": conf.get('test_data', 'password')
        }
        response = requests.post(url=url, headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers["Authorization"] = "Bearer " + token
        id = jsonpath(res, '$..id')[0]
        cls.member_id = id
        cls.headers = headers

    @classmethod
    def add_project(cls):
        # 用例级别的前置: 添加项目
        # 第一步：准备数据
        url = conf.get('env', 'base_url') + '/loan/add'
        params = {
            "member_id": cls.member_id,
            "title": "实现自由",
            "amount": "10000",
            "loan_rate": "18.0",
            "loan_term": "6",
            "loan_date_type": "1",
            "bidding_days": "5"
        }
        # 第二步：请求添加项目的接口
        response = requests.post(url=url, json=params, headers=cls.headers)
        res = response.json()
        # 第三步：提取项目的id
        # 存放在类对象
        id = jsonpath(res, "$..id")[0]
        cls.loan_id = id

    @classmethod
    def aduit(cls):
        # 用例级别的前置: 添加项目
        # 第一步：准备数据
        url = conf.get('env', 'base_url') + '/loan/audit'
        params = {
            "loan_id":cls.loan_id,
            "approved_or_not":True
        }
        # 第二步：请求添加项目的接口
        res = requests.patch(url=url, json=params, headers=cls.admin_headers)
        print(res.json())
