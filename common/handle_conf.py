import os.path
from configparser import ConfigParser
from common.handler_path import CONF_DIR
class Config(ConfigParser):
    """在创建对象的时候，直接加载配置文件的内容"""
    def __init__(self,conf_file):
        super().__init__()
        self.read(conf_file,encoding='utf-8')

conf = Config(os.path.join(CONF_DIR,'conf.ini'))

if __name__ == "__main__":

        #conf = ConfigParser()
        # conf.read(r'E:\python学习\unittest学习\py35_day05\conf.ini',encoding="utf-8")
        conf = Config(r'E:\python学习\unittest学习\py35_day05\conf.ini')



        # name =conf.get('logging', 'name')
        # level =conf.get('logging', 'level')
        # sh_level =conf.get('logging', 'sh_level')
        # fh_level =conf.get('logging', 'fh_level')
        # filename =conf.get('logging', 'filename')

