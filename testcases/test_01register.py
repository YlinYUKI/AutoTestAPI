import os.path
import unittest
import requests
import random
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handler_path import DATA_DIR
from common.handle_conf import conf
from common.handler_log import my_log
from common.handle_mysql import HandleDB
from common.tools import replace_data
@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR,'testCase.xlsx'),'register')
    # 读取用例数据
    cases = excel.read_excel()
    # 项目的基本地址
    base_url = conf.get('env', 'base_url')
    # 请求头
    #读取配置文件的出来的是字符串
    #get方法请求出来的是字符串
    headers = eval(conf.get('env','headers'))
    #使用数据
    db = HandleDB()

    @list_data(cases)
    def test_register(self,item):
        #第一步：准备用例数据
        #1、接口地址
        url = self.base_url + item['url']
        #2、接口请求参数
        # 判断是否有手机号需要替换
        if '#mobile#' in item['data']:
            # 保存成类属性进行替换
            setattr(TestRegister, 'mobile', self.random_mobile()) #动态给一个类属性
            item['data'] = replace_data(item['data'], TestRegister)

        expected = eval(item['expected'])
        params = eval(item['data'])
        if 'mobile_phone' in item['data']:
            sql = 'SELECT * FROM futureloan.member where mobile_phone ="{}"'.format(params['mobile_phone'])
        #3、请求头
        #4、请求方法   ,  转换为小写
        method = item['method'].lower()
        #5、预期结果
        #第二步：请求接口
        response = requests.request(method,url,json=params,headers=self.headers)
        res = response.json()
        #查询手机号是否注册成功
        if 'mobile_phone' in item['data']:
            register = self.db.find(sql)
            print("数据库返回结果", register)
        #第三步：断言
        print("预期结果",expected)
        print("实际结果",res)
        try:
            # 断言code和msg字段是否一致
            self.assertDictIn(expected,res)
            if res['msg'] == 'OK':
                self.assertEqual(register,1)
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


    def random_mobile(self):
        """随机生成手机号码"""
        moblie = "133"
        phone = str(random.randint(13300000000,13399999999))
        return phone