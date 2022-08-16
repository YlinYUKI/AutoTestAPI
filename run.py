import unittest
from unittestreport import TestRunner
from common.handler_path import CASE_DIR, REPORT_DIR

def main():
    # 程序的入口函数
    suite = unittest.defaultTestLoader.discover(CASE_DIR)

    runner = TestRunner(suite,
                        filename='TestAPI',
                        report_dir=REPORT_DIR,
                        tester='YLinG',
                        title='接口测试')

    runner.run()

    # 将测试结果发送到邮箱（发送给一个人）
    runner.send_email(host="smtp.qq.com",
                      port=465,
                      user='846851656@qq.com',
                      # 授权码
                      password='emhbizczawntbfhi',
                      to_addrs='yangzhaolinng@yeah.net',
                      is_file=True)

    # 还可以发送到企业微信

    # 将测试结果发送到邮箱（多个人）
    # runner.send_email(host="smtp.qq.com",
    #                   port=465,
    #                   user='846851656@qq.com',
    #                   # 授权码
    #                   password='emhbizczawntbfhi',
    #                   to_addrs=['yangzhaolinng@yeah.net', "913197057@qq.com","1915274659@qq.com"],
    #                   is_file=True)



if __name__ == '__main__':
    main()

"""
扩展知识
一、测试结果的推送
    1、通过邮件发送到相关人员的邮箱
    2、推送测试结果到钉钉群

"""