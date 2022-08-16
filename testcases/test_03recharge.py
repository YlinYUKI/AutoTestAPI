"""
充值的前提： 登录-->提取token
unittest:
    用例级别的前置： setUp
    测试类级别的前置： setUpClass
1秒可以跑5条测试用例接口
        1、提取token,保存为类属性
        2、提取用户id，保存为类属性
    充值测试方法：
       1、动态的替换参数中用户id  （字符串的replace中的参数是要字符串类型）

    注册类的优化
        1、手机号码动态生成,替换到用例参数中

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
class TestRecharge(unittest.TestCase):
    execl = HandleExcel(os.path.join(DATA_DIR,'testCase.xlsx'),'recharge')
    cases = execl.read_excel()
    db = HandleDB()
    #这是个测试类级别前置. 先实现登录之后再方便后面的充值
    @classmethod
    def setUpClass(cls) -> None:
        """用例的前置方法： 登录提取token"""
        # 1、请求登录接口， 进行登录
        url = conf.get('env','base_url')+'/member/login'
        params = {
            "mobile_phone":conf.get("test_data",'mobile'),
            "pwd":conf.get("test_data",'password')
        }
        headers = eval(conf.get("env","headers"))
        response = requests.post(url=url, json=params, headers=headers)
        res = response.json()
        #2、登录成功后再提取token
        #使用jsonpath定位到token
        token = jsonpath(res,'$..token')[0]  #jsonpath提取出来是列表要索引取值为字符串
        print(token)
        # 将token添加到请求头中
        headers["Authorization"] = "Bearer " + token
        #设置为类属性，方便后面调用  保存含有token的请求头类属性
        cls.headers = headers
        #3、提取用户的id给充值接口使用
        cls.member_id = jsonpath(res,'$..id')[0]

    @list_data(cases)
    def test_recharge(self,item):
        #第一步、准备数据
        url = conf.get("env", "base_url")+ item["url"]
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone = "{}"'.format(conf.get('test_data','mobile'))
#-------------------------------------------------------------------------------------------------------------------------------
        if "#member_id#" in item['data']:
            # 动态处理需要替换的用户的参数
            # item['data'] = item['data'].replace('#member_id#',str(self.member_id)) #使用replace需要是字符串类型的， 因为返回的member_id是int了类所有要转换
            item['data'] = replace_data(item['data'], TestRecharge)
#----------------------------------------------------------------------------------------------------------------------------------
        #=========================请求接口之前查询余额=====================================
        #执行sql查询余额
        start_amount = self.db.find_one(sql)[0]
        print(start_amount)
        params = eval(item['data'])
        expected = eval(item["expected"])
        method = item['method'].lower()
        #第二步、发送请求，获取接口返回的数据
        response = requests.request(method,url, json=params, headers=self.headers)
        res = response.json()
        print("预期结果：",expected)
        print("实际结果：",res)
        #==================================请求接口之后查询用户余额===================================================
        #执行sql查询余额
        end_amount = self.db.find_one(sql)[0] #返回元组要提取出来
        print(end_amount)
        #第三步、断言
        try:
            #判断code,msg字段是否一致
            self.assertDictIn(expected,res)
            #========================检验数据库中用户余额的变化是否等于充值的金额===================================================
            #充值成功，用户余额变化为充值金额
            if res['msg'] == 'OK':
                change = float(end_amount - start_amount)
                print(change)
                self.assertEqual(change, float(params['amount']))
            #充值失败.变化为0
            else:
                change = float(end_amount - start_amount)
                self.assertEqual(change, 0)
        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.error(e)
            #抛出异常
            raise e
        else:
            my_log.info("用例--【{}】---执行成功".format(item['title']))

    """判断是否在里面"""
    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            """字典成员运算的逻辑"""
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))