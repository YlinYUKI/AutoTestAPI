"""
    项目的审核 ： 管理员进行审核

审核的前置条件：
    1、管理员登录（类级别的前置）
    2、创建一个项目 （用例级别前置）
"""
import os
import unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handler_log import my_log
from common.handle_mysql import HandleDB
@ddt
class TestAudit(unittest.TestCase):
    execl = HandleExcel(os.path.join(DATA_DIR,'testCase.xlsx'),'audit')
    cases = execl.read_excel()
    db = HandleDB()
    @classmethod
    def setUpClass(cls) -> None:
        #----------------------管理员登录-------------------------------
        url = conf.get('env', 'base_url')+'/member/login'
        headers = eval(conf.get('env', 'headers'))
        params = {
            "mobile_phone":conf.get('test_data', 'admin_mobile'),
            "pwd":conf.get('test_data', 'admin_pwd')
        }
        response = requests.post(url=url, headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers["Authorization"] = "Bearer " + token
        id = jsonpath(res, '$..id')[0]
        cls.admin_member_id = id
        cls.admin_headers = headers

        #--------------------用户登录----------------------------
        url = conf.get('env', 'base_url')+'/member/login'
        headers = eval(conf.get('env', 'headers'))
        params = {
            "mobile_phone":conf.get('test_data', 'mobile'),
            "pwd":conf.get('test_data', 'password')
        }
        response = requests.post(url=url, headers=headers, json=params)
        res = response.json()
        token = jsonpath(res, '$..token')[0]
        headers["Authorization"] = "Bearer " + token
        id = jsonpath(res, '$..id')[0]
        cls.member_id = id
        cls.headers = headers

    def setUp(self) -> None:
        # 用例级别的前置: 添加项目
        # 第一步：准备数据
        url = conf.get('env', 'base_url') + '/loan/add'
        params = {
             "member_id": self.member_id,
             "title": "实现自由",
             "amount": "10000",
             "loan_rate": "18.0",
             "loan_term": "6",
             "loan_date_type": "1",
             "bidding_days": "5"
        }

        # 第二步：请求添加项目的接口
        response = requests.post(url=url, json=params, headers= self.headers)
        res = response.json()
        # 第三步：提取项目的id
        # 存放在类对象
        id = jsonpath(res, "$..id")[0]
        TestAudit.loan_id = id
        self.loan = id

    @list_data(cases)
    def test_audit(self, item):
        # 第一步: 准备数据
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'],TestAudit)
        params = eval(item['data'])
        method = item['method']
        expected = eval(item['expected'])
        # 第二步： 请求接口
        response = requests.request(method=method, url=url, json=params, headers=self.admin_headers)
        res = response.json()

        # 判断是否是审核通过的用例， 并且审核通过，如果是则保存项目id为审核通过项目的id
        if item['title'] == '审核通过' and res ['msg'] == 'OK':
            TestAudit.pass_loan_id = self.loan


        # 断言
        print("预期结果", expected)
        print("实际结果", res)
        #第三步、断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if res['msg'] == 'OK':
                sql = 'SELECT status FROM futureloan.loan WHERE id={} ORDER BY create_time DESC'.format(self.loan)
                print(sql)
                status = self.db.find_one(sql)[0]
                self.assertEqual(expected['status'], status)

        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.error(e)
            raise e #抛出异常让unittest接收
        else:
            my_log.info("用例--【{}】---执行成功".format(item["title"]))



