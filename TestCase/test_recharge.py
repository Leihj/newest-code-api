# -*- coding: utf-8 -*-
# @File    : test_recharge.PY
# @Date    : 2019/7/19-15:24
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

"""
充值模块： 1、断言---预期结果和实际结果的比对
          2、数据库的验证---充值金额=充值后的金额-充值前的金额
"""
import json
import unittest
from common.do_excel import Do_Excel
from common import contants_path
from common.api_request import Session_api
from ddt import ddt,data,unpack
from common.logger import get_log
from common.re_reflect import Context
from common.do_mysql import Do_Mysql

logger=get_log(__name__)
@ddt
class Register_Test(unittest.TestCase):
    excel=Do_Excel(contants_path.excel_dir,2)
    cases=excel.read_excel()
    @classmethod
    def setUpClass(cls):
        cls.http_request=Session_api()
        cls.DB=Do_Mysql()
    @data(*cases)
    def test_recharge(self,case):
        logger.info("----测试用例 {}开始执行----".format(case.title))
        case.data=Context().replace(case.data)
        print(case.data)
        if case.check_sql:
            #获取充值前的金额 ---excel取出来的数据是字符串，要用eval函数转成字典后，获取字典的value值
            money=self.DB.fetch_one(eval(case.check_sql)["sql1"])
            before_money=money["LeaveAmount"]
            logger.info("充值前的金额{}".format(type(before_money)))

        resp=self.http_request.api(method=case.method,url=case.url,data=case.data)

        try:
            self.assertEqual(str(case.expected),resp.json()['code'])
            Do_Excel(contants_path.excel_dir,2).write_excel(case.case_id+1,resp.text,"PASS")
            if case.check_sql:
                # 获取充值前的金额 ---excel取出来的数据是字符串，要用eval函数转成字典后，获取字典的value值
                money = self.DB.fetch_one(eval(case.check_sql)["sql1"])
                after_money=money["LeaveAmount"]
                logger.info("充值后的金额{}".format(type(after_money)))
                amount=(eval(case.data))["amount"]
                #数据库的断言，用充值后的金额-充值前的金额=实际充值的金额
                #amount转换后取到的类型是int型，转成float型，充值前的金额和充值后的金额全部转成float，然后再金额结果的比对
                self.assertEqual(float(amount),(float(after_money)-float(before_money)))
                print("最后充值的金额是{}".format(float(after_money)-float(before_money))) #最后获取的金额的类型是浮点型
        except AssertionError as e:
            Do_Excel(contants_path.excel_dir, 2).write_excel(case.case_id + 1, resp.text, "FAILED")
            logger.error("---测试预期结果和实际结果不一致！！---".format(e))
            raise e
        logger.info("-----测试结束了-----")

    @classmethod
    def tearDownClass(cls):
        cls.http_request.close()
        cls.DB.close()
        logger.info("----测试后置结束----")

if __name__ == '__main__':
    unittest.main()