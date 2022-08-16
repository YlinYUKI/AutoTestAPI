# AutoTestAPI
这是一个接口自动化框架
采用了unittest + request + openxl + pymysql + unittestreports +logging 进行接口自动化框架的搭建，实现自动从excel进行数据的读取发送接口进行校验 测试后形成测试报告并有日志

common中存放的是公共方法 包括如下:
    handle_path : 采用os模块 处理了各个模块中会用的路径 将他们处理为绝对路径 方便在其他环境下项目可以使用
    handle_conf : 采用python中configparser的模块 实现对conf.ini存放的配置文件中数据进行读取 (如基础url mysql的配置 logging日志模块的配置) 
    handle_excel : 采用openxl模块对excel文件进行读取 （注意读取出来的是字符串类型 如果是存放的字典类型的话 要用eval进行转换）
    handle_log : 采用python中的logging模块 创建一个日志收集器 实现对每天测试用例进行日志收集
    handle_mysql : 采用python中的pymysql模块 实现对mysql数据库的连接 并能进行语句查询 实现在testcases中的数据校验 （注意返回的是元组需要提取出来）
    tools ： 采用re模块的正则表达式 因为在接口中存在一些用例之间的关联 如之前创建的商品id 后面需要审核 那么可以在excel中先用 #id# 来存储 在执行用例的时候 用tools中封装的方法进行替换。
    
conf 中存放的是一些配置文件

datas 中存放测试用例 （注意格式要规范）

logs 中存放的是日志

reports 中存放用例报告 采用unittestreport来实现的

testcases 中放的就是测试用例 实现有 登录 注册 充值 取现 用户信息 投资 添加 审核模块的测试用例编写 
    中采用到了 ddt 数据驱动的方法 实现每天用例来执行测试用例
    还有 测试夹具的使用 比如类前置方法 用例前置方法
    用jsonpath 来提取token id 等 （注意提取出来的是一个列表要 用索引进行读取）

run.py 是整个文件的入口   采用 TestSuit(测试套件)，用来管理 组装多个 TestCase(测试用例)

                               TestRunner(测试执行，测试运行) 用来去执行 TestSuite(测试套件)的用例
                               
                               还有使用unittestreport中功能的将测试结果发送到邮箱

下载到本地即可使用 运行入口是run.py 如果要用到别的项目 common中的方法是通用的 只需修改conf中的配置文件 以及testcases中的测试用例即可

希望能到支持~~~
