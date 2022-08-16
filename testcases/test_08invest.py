"""
前置操作：
    1. 普通用户登录（类级别）
    2. 管理员登录（类级别）
    3. 添加项目（类级别）
    4. 审核项目（类级别）

    用例方法：
    1、准备数据
    2、发送请求
    3、断言

    # 数据校验
        用户表：用户的余额投资前后会变化
            投资前 - 投资后 = 投资金额


        流水记录表： 投资成功会新增一条流水记录
            投资后用户的流水记录的数量 - 投资前用户流水记录数量 ==1


        投资表： 投资成功会新增一条记录
            投资后用户的流水记录的数量 - 投资前用户流水记录数量 ==1

        ---------扩展投资后（可投金额为0）满标的情况，会生成回款计划------------
        1、 先把项目的投资记录id都查出来
        2、 遍历投资记录id
        3、 根据每个投资记录的id去查询回款计划表：


"""

import unittest
import os
import requests
from unittestreport import ddt,list_data
from common.handle_mysql import HandleDB
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handler_log import my_log
from common.handle_conf import conf
from testcases.fixture import BaseTest
from common.tools import replace_data
@ddt
class TestInvest(unittest.TestCase,BaseTest):
    excel = HandleExcel(os.path.join(DATA_DIR, 'testCase.xlsx'),'invest')
    db = HandleDB()
    cases = excel.read_excel()
    @classmethod
    def setUpClass(cls) -> None:
        # 管理员登录
        cls.admin_login()
        # 普通用户登录
        cls.user_login()
        # 添加项目
        cls.add_project()
        # 审核
        cls.aduit()
    @list_data(cases)
    def test_invest(self,item):
        # 第一步：准备用例数据
        url = conf.get('env', 'base_url')+item['url']
        item['data'] = replace_data(item['data'], TestInvest)
        expected = eval(item['expected'])
        method = item['method']
        params = eval(item['data'])
        #----------------------投资前查询数据库--------------
        # 查询用户表的sql
        sql1 ='SELECT leave_amount FROM futureloan.member WHERE mobile_phone = "{}"'.format(conf.get('test_data','mobile'))
        # 查询投资表的sql
        sql2 = 'SELECT id FROM futureloan.invest WHERE member_id = "{}"'.format(self.member_id)
        # 查询流水表的sql
        sql3 = 'SELECT id FROM futureloan.financelog WHERE pay_member_id = "{}"'.format(self.member_id)
        s_amount = self.db.find_one(sql1)[0]
        s_invest = self.db.find(sql2)
        s_financelog =self.db.find(sql3)
        # 第二步： 发送请求
        response = requests.request(url=url,method=method, json=params, headers=self.headers)
        res = response.json()
        # ------------------------投资后查询数据库------------------------------
        # 第三步: 断言
        # 断言

        s_amount1 = self.db.find_one(sql1)[0]
        s_invest2 = self.db.find(sql2)
        s_financelog3 =self.db.find(sql3)

        print("预期结果", expected)
        print("实际结果", res)
        #第三步、断言
        try:
            self.assertEqual(expected['code'], res['code'])
            # 断言实际结果中的msg是否包含 预期结果中msg中的内容
            self.assertIn(expected['msg'], res['msg'])
            if res['msg']=='OK':
                # 断言用户余额
                self.assertEqual(float(s_amount-s_amount1),float(params['amount']))
                # 断言投资记录
                self.assertEqual(s_invest2-s_invest, 1)
                self.assertEqual(s_financelog3-s_financelog, 1)

        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.error(e)
            raise e #抛出异常让unittest接收
        else:
            my_log.info("用例--【{}】---执行成功".format(item["title"]))

# self 是实例方法的第一个参数, 代表的是实例对象本身
# cls  是类方法的第一个参数, 代表的是类的本身