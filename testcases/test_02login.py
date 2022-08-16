import os.path
import unittest
import requests
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_conf import conf
from common.handler_log import my_log
@ddt
class TestLogin(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR,'testCase.xlsx'),'login')
    # 读取用例数据
    cases = excel.read_excel()
    # 项目的基本地址
    base_url = conf.get('env', 'base_url')
    # 请求头
    #读取配置文件的出来的是字符串
    #get方法请求出来的是字符串
    headers = eval(conf.get('env','headers'))

    @list_data(cases)
    def test_login(self,item):
        #第一步：准备用例数据
        #1、接口地址
        url = self.base_url + item['url']
        #2、接口请求参数
        expected = eval(item['expected'])
        params = eval(item['data'])
        #3、请求头
        #4、请求方法   ,  转换为小写
        method = item['method'].lower()
        #5、预期结果
        #第二步：请求接口
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        #第三步：断言
        print("预期结果",expected)
        print("实际结果",res['code'])
        try:
            # 断言code和msg字段是否一致
            self.assertDictIn(expected,res)
        except AssertionError as e:
            # 记录日志
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.error(e)
            # 回写结果到excel（根据实际需求写不写到excel结果中） #回写到excel需要大量时间

            raise e
        else:
            my_log.info("用例--【{}】---执行成功".format(item['title']))

    #判断是否在里面
    def assertDictIn(self, expected, res):
        for k,v in expected.items():
            """字典成员运算的逻辑"""
            if  res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected,res))