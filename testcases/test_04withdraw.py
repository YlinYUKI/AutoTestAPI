"""
取现的前提： 登录-->提取token
unittest:
    用例级别的前置： setUp
    测试类级别的前置： setUpClass
1秒可以跑5条测试用例接口
        1、提取token,保存为类属性
        2、提取用户id，保存为类属性
    取现测试方法：
       1、动态的替换参数中用户id  （字符串的replace中的参数是要字符串类型）

"""
import os
import unittest
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_conf import conf
from common.handler_log import my_log
from common.handle_mysql import HandleDB
from common.tools import replace_data
@ddt
class TestWithdraw(unittest.TestCase):
    #从excel中读取出数据
    excel = HandleExcel(os.path.join(DATA_DIR,'testCase.xlsx'),'withdraw')
    cases = excel.read_excel()
    # 初始化数据库
    db = HandleDB()

    #这是个测试类级别前置. 先实现登录之后再方便后面的提现
    @classmethod
    def setUpClass(cls) -> None:
        """用例的前置方法： 登录提取token"""
        # 1、请求登录接口， 进行登录
        url = conf.get('env',"base_url")+'/member/login'
        params = {
            "mobile_phone":conf.get("test_data","mobile"),
            "pwd":conf.get("test_data","password")
        }
        #headers 因为使用get方法得到的是字符串，所以要转换为字典
        headers = eval(conf.get('env',"headers"))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        #2、登录成功后再提取token
        #使用jsonpath提取token
        token = jsonpath(res,'$..token')[0] #因为传回来的是列表要将它提取出来
        #将提取到token加入到headers里面
        headers['Authorization'] = "Bearer " + token
        #设置为类属性，方便后面调用  保存含有token的请求头类属性
        cls.headers = headers
        cls.member_id = jsonpath(res,'$..id')[0] #因为传回来的是列表要将它提取出来



    @list_data(cases)
    def test_withdraw(self,item):
        #第一步、准备数据
        url = conf.get('env','base_url')+item["url"]
        method = item['method'].lower()
        expected = eval(item['expected'])
        #===========================取现前要查询查询数据库用户账户金额===========================================
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone = "{}"'.format(conf.get('test_data', 'mobile'))
        # 执行sql查询金额
        start_amount = self.db.find_one(sql)[0] #返回的是一个元组所有要取出来

#---------------------动态处理数据--------------------------------------------------------------
        if "#member_id#" in item['data']:
            # item['data'] = item['data'].replace("#member_id#",str(self.member_id)) #使用replace需要是字符串类型的， 因为返回的member_id是int了类所有要转换
            item['data'] = replace_data(item['data'], TestWithdraw)
#----------------------------------------------------------------------------------------------------------
        params = eval(item['data'])
        # 第二步、发送请求，获取接口返回的数据
        response = requests.request(method, url, json=params, headers=self.headers)
        res = response.json()
        # =============================取现之后查询数据库用户的金额====================================================
        #执行sql语句
        end_amount = self.db.find_one(sql)[0] #因为是元组所有要取出来
        print("预期结果", expected)
        print("实际结果", res)
        #第三步、断言
        try:
            self.assertDictIn(expected,res)
            change = float(start_amount - end_amount)
            print(change)
            if res['msg'] == 'OK':
                self.assertEqual(change,float(params['amount']))
            else:
                self.assertEqual(change,0)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item["title"]))
            my_log.error(e)
            raise e #抛出异常让unittest接收
        else:
            my_log.info("用例--【{}】---执行成功".format(item["title"]))



    """判断是否在里面"""
    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            """字典成员运算的逻辑"""
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))