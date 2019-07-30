# -*- coding: utf-8 -*-
# @File    : conf_test.PY
# @Date    : 2019/7/9-10:17
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

from configparser import ConfigParser
from common import contants_path

class Conf:
    def __init__(self):
        self.config=ConfigParser()  #初始化config库
        self.config.read(contants_path.switch_path,encoding="utf-8")   #先加载global文件的配置
        switch =self.config.getboolean("switch","off")

        # 根据switch的开关项选择测试环境还是线上环境
        if switch:
            self.config.read(contants_path.test_path,encoding="utf-8")  #当switch为True时，选择测试环境
        else:
            self.config.read(contants_path.online_path,encoding="utf-8")   #当switch为False时，选择线上环境

    #得到所有的section，并以列表的形式返回
    def get_section(self):
        return self.config.sections()

    #得到该section的所有option
    def get_option(self,section):
        return self.config.options(section)

    #得到该section的所有键值对
    def get_item(self,section):
        return self.config.items(section)

    #得到section中option的值，返回为string类型
    def get_str(self,section,option):
        return self.config.get(section,option)

    #得到section中option的值，返回为int类型
    def get_int(self,section, option):
        return self.config.getint(section, option)

    # 得到section中option的值，返回为浮点型类型
    def get_float(self,section, option):
        return self.config.getfloat(section, option)

    # 得到section中option的值，返回为布尔型类型（True/False）
    def get_boolean(self,section, option):
        return self.config.getboolean(section, option)


    #得到section中option的值，返回为python能够识别的数据类型
    def get_eval(self,section, option):
        return eval(self.config.get(section, option))

config=Conf()


if __name__ == '__main__':
    print("section",config.get_section())
    # print("option",config.get_option("data"))
    print("itme",config.get_item("data1"))