# -*- coding: utf-8 -*-
# @File    : test_withdraw.PY
# @Date    : 2019/7/24-18:20
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

"""提现模块"""
import json
import unittest
from common.do_excel import Do_Excel
from common import contants_path
from common.api_request import Session_api
from ddt import ddt,data,unpack
from common.logger import get_log
from common.do_mysql import Do_Mysql
from common.re_reflect import  Context


logger=get_log(__name__)
@ddt
class Withdraw_Test(unittest.TestCase):
    excel=Do_Excel(contants_path.excel_dir,3)
    cases=excel.read_excel()

    @classmethod
    def setUpClass(cls):
        logger.info("----测试前置开始-----")
        cls.http_request=Session_api()
        cls.DB=Do_Mysql()

    @data(*cases)
    def test_withdraw(self,case):
        logger.info("----测试用例 {}开始，第{}行用例".format(case.title,case.case_id+1))
        case.data=Context().replace(case.data)  #将配置文件的数据反射到excel表格中
        if case.check_sql:  #如果sql语句不为空，则执行sql语句
            money=self.DB.fetch_one(eval(case.check_sql)['sql1'])
            before_money=money['LeaveAmount']
            print("提现前卡里的余额{}".format(before_money))
        resp=self.http_request.api(case.method,case.url,case.data)
        resp_text=(json.loads(resp.text))['code']   #将json格式转换成字典，然后取出code的值
        try:
            print('resp_text',resp_text)
            self.assertEqual(case.expected,int(resp_text))  #将字符串类型转换成int类型
            Do_Excel(contants_path.excel_dir, 3).write_excel(case.case_id + 1, resp.text, 'PASS')
            if case.check_sql:
                money=self.DB.fetch_one(eval(case.check_sql)['sql1'])
                after_money=money['LeaveAmount']
                print("提现后卡里的余额{}".format(after_money))
                amount=eval(case.data)['amount']
                self.assertEqual(float(amount),float(before_money)-float(after_money))
                logger.info("数据库验证：最后提现的金额是{}".format(float(before_money)-float(after_money)))
        except AssertionError as e :
            Do_Excel(contants_path.excel_dir, 3).write_excel(case.case_id + 1, resp.text, 'FAILED')
            logger.error("---测试预期结果和实际结果不一致！！---".format(e,case.case_id))
            raise e
        logger.info("-----测试结束了------")

    @classmethod
    def tearDownClass(cls):
        logger.info("----测试结束了-----")
        cls.http_request.close()


if __name__ == '__main__':
    unittest.main()