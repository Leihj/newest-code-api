# -*- coding: utf-8 -*-
# @File    : contants.PY
# @Date    : 2019/7/9-10:44
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import os

#os.path.realpath(__file__)  返回真实路径
#os.path.dirname 返回上一层路径

base_dir=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))   #找到根目录
print(base_dir)

switch_path=os.path.join(base_dir,"conf","global.conf")  #配置文件--切换环境开关项

test_path=os.path.join(base_dir,"conf","test_data.conf")  #配置文件--测试环境的路径

online_path=os.path.join(base_dir,"conf","online_data.conf")  #配置文件--正式环境的路径

all_log=os.path.join(base_dir,"test_result","all_log")    #收集全部日志的文件夹路径

err_log=os.path.join(base_dir,"test_result","error_log")    #只收集error日志的文件夹路径

excel_dir=os.path.join(base_dir,"test_data","Future_loans.xlsx")  #excel--测试用例的路径

report_path=os.path.join(base_dir,"test_result","html_report")    #html测试报告路径

