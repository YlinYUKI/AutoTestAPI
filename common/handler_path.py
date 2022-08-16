"""
此模块专门处理项目中的绝对路径
"""
import os

# 项目根目录的绝对路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例数据所在目录：
DATA_DIR = os.path.join(BASE_PATH,'datas')

# 配置文件的根目录
CONF_DIR =os.path.join(BASE_PATH,'conf')

# 日志文件所在目录
LOG_DIR =  os.path.join(BASE_PATH,'logs')

# 报告所在路径
REPORT_DIR = os.path.join(BASE_PATH,'reports')

# 用例模块所在目录
CASE_DIR = os.path.join(BASE_PATH,'testcases')