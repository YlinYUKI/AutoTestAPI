import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handler_log import my_log
from common.handle_mysql import HandleDB
"""
添加项目：前提是要登录
    定义用例的前置方法（类级别）
    
"""

@ddt
class Testadd(unittest.TestCase):
    db = HandleDB()
    excel = HandleExcel(os.path.join(DATA_DIR, 'testCase.xlsx'),'add')
    case = excel.read_excel()
    @classmethod
    def setUpClass(cls) -> None:
        """登录"""
        # 1、准备登录的数据
        url = conf.get('env', 'base_url') +'/member/login'
        params ={
            "mobile_phone":conf.get("test_data", "mobile"),
            "pwd":conf.get("test_data", 'password')
        }

        headers= eval(conf.get('env', 'headers'))
        # 2、请求登录接口
        reponse = requests.post(url,json=params, headers=headers)
        res = reponse.json()
        # 3、提取token， 放到请求头中
        token = jsonpath(res, '$..token')[0]
        id = jsonpath(res, '$..id')[0]
        headers["Authorization"] = "Bearer " + token
        # 4、提取用户id
        cls.member_id = id
        cls.headers = headers



    @list_data(case)
    def test_add(self, item):
        # 第一步：准备数据
        url = conf.get('env', 'base_url') + item['url']
        item['data'] = replace_data(item['data'], Testadd)
        method = item['method']
        params = eval(item['data'])
        expected = eval(item['expected'])
        # 调用接口前,查询数据库该用户的项目数量
        sql = 'SELECT * FROM futureloan.loan WHERE member_id={}'.format(self.member_id)
        # 查询调用前有几条数据
        start = self.db.find(sql)
        # 第二步：调用接口，获得实际结果
        response = requests.request(method=method,url=url,json=params,headers=self.headers)
        res = response.json()
        end = self.db.find(sql)
        # 第三步： 断言
        print('预期结果',expected)
        print("实际结果",res)
        try:
            self.assertDictIn(expected,res)
            # 成功的话会新增一条
            if res['msg'] == 'OK':
                self.assertEqual(end-start, 1)
            else:
                self.assertEqual(end-start, 0)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.error(e)
            #抛出异常
            raise e
        else:
            my_log.info("用例--【{}】---执行成功".format(item['title']))





 # ==============================================================================================================
        """判断是否在里面"""
    def assertDictIn(self, expected, res):
            for k, v in expected.items():
                """字典成员运算的逻辑"""
                if res.get(k) == v:
                    pass
                else:
                    raise AssertionError("{} not in {}".format(expected, res))