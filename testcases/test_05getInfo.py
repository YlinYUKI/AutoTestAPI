"""
查看的前提： 登录-->提取token
unittest:
    用例级别的前置： setUp
    测试类级别的前置： setUpClass
1秒可以跑5条测试用例接口
        1、提取token,保存为类属性
        2、提取用户id，保存为类属性
    替换测试方法：
       1、动态的替换参数中用户id  （字符串的replace中的参数是要字符串类型）

"""
import unittest
import requests
import os
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.tools import replace_data
from common.handler_log import my_log
@ddt
class TestInfo(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "testCase.xlsx"), "get")
    case  = excel.read_excel()
    # 先登录提取token
    @classmethod
    def setUpClass(cls) -> None:
        """测试类级别前置 登录提取token"""
        # 1. 登录提取token
        url = conf.get("env", "base_url") + '/member/login'
        params = {
            "mobile_phone":conf.get("test_data","mobile"),
            "pwd":conf.get("test_data","password")
        }
        # 因为从配置环境中读取的是字符串类型的，所以要用eval来讲它转换为字符串类型
        headers = eval(conf.get("env", "headers"))
        response = requests.post(url, json=params, headers=headers)
        res = response.json()
        # 2. 登录成功之后提取token
        # 提取token
        token = jsonpath(res, "$..token")[0] # 因为取出来是元组所以要取值
        headers["Authorization"] = "Bearer " + token
        # 提取id
        id = jsonpath(res,"$..id")[0]
        cls.member_id = id
        cls.headers = headers

    # 开始执行用例
    @list_data(case)
    def test_info(self, item):
        # 1.准备用例数据
        url = conf.get("env", "base_url")+item["url"]
        if "#member_id#" in item["data"]:
            item['data'] = replace_data(item['data'], TestInfo)
        id = eval(item['data'])['member_id']
        url = url.format(id)
        method = item['method'].lower()
        expected = eval(item['expected'])
        # 2.发送请求, 返回结果
        response = requests.request(method,url,headers=self.headers)
        # 返回的json是字典格式的
        res = response.json()
        # 3.进行断言
        print("预期结果",expected)
        print("实际结果",res)
        # 进行断言,如果异常进行报错
        try:
            # 判断code, msg字段是否一致
            self.assertDictIn(expected, res)

        except AssertionError as e:
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.error(e)
            #抛出异常
            raise e
        else:
            my_log.info("用例--【{}】---执行成功".format(item['title']))



#=================================================================================================================
            """判断是否在里面"""
    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            """字典成员运算的逻辑"""
            if res.get(k) == v:
                    pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))



