# -*- coding: utf-8 -*-
# @File    : test_invst.PY
# @Date    : 2019/7/31-16:17
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import unittest
from common.do_excel import Do_Excel
from common import contants_path
from common.api_request import Session_api
from ddt import ddt,data,unpack
from common.logger import get_log
from common.re_reflect import Context
from common.do_mysql import Do_Mysql

@ddt
class InvestTest(unittest.TestCase):
    excel = Do_Excel(contants_path.excel_dir, 4)
    cases = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        cls.http_request = Session_api()
        cls.DB = Do_Mysql()

    @data(*cases)
    def test_invest(self, case):
        print("开始执行测试：", case.title)
        # 在请求之前替换参数化的值
        case.data = Context().replace(case.data)
        resp = self.http_request.api(case.method, case.url, case.data)
        try:
            self.assertEqual(str(case.expected), resp.json()['code'])
            self.excel.write_excel(case.case_id + 1, resp.text, 'PASS')

            # 判断加标成功之后，查询数据库，取到loan_id
            if resp.json()['msg'] == "加标成功":
                sql = {'sql1': 'SELECT * FROM future.loan  WHERE memberId="93870" ORDER BY id DESC LIMIT 1'}
                loan_id = self.DB.fetch_one(sql)['sql']
                print('标的ID：', loan_id)
                # 保存到类属性里面
                setattr(Context, "loan_id", str(loan_id))
        except AssertionError as e:
            self.excel.write_excel(case.case_id + 1, resp.text, 'FAIL')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()