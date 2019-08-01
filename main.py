# -*- coding: utf-8 -*-
# @File    : main.PY
# @Date    : 2019/7/8-16:11
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import sys
sys.path.append('./')
print("系统路径",sys.path)

import unittest
from common import contants_path
from common import HTMLTestRunnerNew

import time
discover=unittest.defaultTestLoader.discover(contants_path.base_dir,"test_*.py")
with open(contants_path.base_dir+"/TestReport{}.html".format(time.strftime('%Y%m%d%H%M%S')),"wb+")as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner \
        (stream=file, title="auto-test-interface测试报告", description="2019年4月19日", tester="leihj")
    runner.run(discover)