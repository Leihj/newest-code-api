# -*- coding: utf-8 -*-
# @File    : test_login.PY
# @Date    : 2019/7/12-11:47
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import unittest
from common.do_excel import Do_Excel
from common import contants_path
from ddt import ddt,data,unpack
from common.api_request import Session_api
from common.logger import get_log
from common.re_reflect import Context


logger=get_log(__name__)

@ddt
class Login_Test(unittest.TestCase):

    excel=Do_Excel(contants_path.excel_dir,1)
    cases=excel.read_excel()

    @classmethod
    def setUpClass(cls):
        logger.info("----测试前置开始----")
        cls.http_request=Session_api()



    @data(*cases)
    def test_success(self,case):
        logger.info("----测试用例：{}开始执行-----".format(case.title))
        case.data=Context().replace(case.data)
        resp=self.http_request.api(case.method,case.url,case.data)

        try:
            self.assertEqual(case.expected,resp.text)
            Do_Excel(contants_path.excel_dir,1).write_excel(case.case_id+1,resp.text,"PASS")
        except AssertionError as  e:
            Do_Excel(contants_path.excel_dir, 1).write_excel(case.case_id + 1, resp.text, "FAILED")
            logger.info("---测试预期结果和实际结果不一致！！---".format(e))
            raise e
        logger.info("-----测试结束了------")


    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()    #请求关闭
        logger.info("----测试后置结束----")