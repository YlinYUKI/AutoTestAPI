"""
封装一个通过正则进行替换数据
"""

import re
from common.handle_conf import conf
# def replace_data(data, cls):
#     """
#
#     :param data: 要进行替换的用例数据(字符串)
#     :param cls:  测试类
#     :return:
#     """
#     while re.search('#(.+?)#', data): #查不到返回的是None
#         res2 = re.search("#(.+?)#", data)
#         item = res2.group()
#         attr = res2.group(1)
#         value = getattr(cls, attr)
#         # 替换数据
#         data = data.replace(item, str(value))
#     return data

#---------------------------------升级版-------------------------------------------------
def replace_data(data, cls):
    """

    :param data: 要进行替换的用例数据(字符串)
    :param cls:  测试类
    :return:
    """
    while re.search('#(.+?)#', data): #查不到返回的是None
        res2 = re.search("#(.+?)#", data)
        item = res2.group()
        attr = res2.group(1)
        try:
            value = getattr(cls, attr)
        except AttributeError:
            conf.get('test_data', attr)

        # 替换数据
        data = data.replace(item, str(value))
    return data