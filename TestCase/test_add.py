# -*- coding: utf-8 -*-
# @File    : test_add.PY
# @Date    : 2019/7/29-14:39
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import unittest
from common.api_request import Session_api
from common.do_excel import Do_Excel
from common import contants_path
from ddt import ddt,data,unpack
from common.re_reflect import Context
from common.logger import get_log
from  common.do_mysql import Do_Mysql

logger=get_log(__name__)
@ddt
class Add_Test(unittest.TestCase):
    excel=Do_Excel(contants_path.excel_dir,5)
    cases=excel.read_excel()
    @classmethod
    def setUpClass(cls):
        logger.info("----测试前置开始----")
        cls.http_request=Session_api()
        cls.DB=Do_Mysql()

    @data(*cases)
    def test_add(self,case):
        logger.info("----测试用例{}开始执行----".format(case.title))

        case.data=Context().replace(case.data)
        print("casedata",case.data)
        resp = self.http_request.api(case.method,case.url,case.data)
        if case.check_sql:
                before_data=self.DB.fetch_one (eval((case.check_sql))['sql1'])
        try:
            self.assertEqual(case.expected,resp.json()['code'])
            Do_Excel(contants_path.excel_dir,5).write_excel(case.case_id+1,resp.text,"PASS")
            if case.check_sql:
                after_data=self.DB.fetch_one (eval((case.check_sql))['sql1'])
                self.assertEqual(before_data,after_data)
                logger.info("----数据库验证通过！！！-----")
        except AssertionError as e:
            Do_Excel(contants_path.excel_dir,5).write_excel(case.case_id+1,resp.text, "FAILED")
            logger.error("----测试出错了，预期结果！=实际结果")
            raise e
        logger.info("----测试结束了-----")


    @classmethod
    def tearDownClass(cls):
        logger.info("----测试后置结束----")
        cls.http_request.close()
        cls.DB.close()

if __name__ == '__main__':
    unittest.main()
    # sql='SELECT * FROM future.loan WHERE memberId="93870"'