# -*- coding: utf-8 -*-
# @File    : test_bidLoan.PY
# @Date    : 2019/7/31-12:01
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

logger=get_log(__name__)
@ddt
class BidLoan_Test(unittest.TestCase):
    excel=Do_Excel(contants_path.excel_dir,4)
    cases=excel.read_excel()


    @classmethod
    def setUpClass(cls):
        logger.info("----测试前置准备----")
        cls.http_request=Session_api()
        cls.DB=Do_Mysql()

    @data(*cases)
    def test_bidload(self,case):
        logger.info("----测试用例：{}开始执行----".format(case.title))
        case.data=Context().replace(case.data)
        if case.check_sql:
            money = self.DB.fetch_one(eval(case.check_sql)["sql1"])
            print(money)
            invest_before=money['LeaveAmount']
        resp=self.http_request.api(case.method,case.url,case.data)
        actual=resp.json()['code']
        print(resp.text)
        print("actual",type(actual))
        try:
            self.assertEqual(str(case.expected),actual)
            Do_Excel(contants_path.excel_dir,4).write_excel(case.case_id+1,resp.text,"PASS")
            if resp.json()['msg']=='加标成功':
                sql='SELECT ID FROM future.loan  WHERE memberId="93870" ORDER BY id DESC LIMIT 1'
                loan_id=self.DB.fetch_one(sql)['ID']    #返回的是字典，根据字典去对应的值
                setattr(Context,"loan_id",str(loan_id)) #如果属性不存在会创建一个新的对象属性，并对属性赋值
            if case.check_sql: #验证数据库
                money = self.DB.fetch_one(eval(case.check_sql))['sql1']
                invest_after = money['LeaveAmount']
                amout=eval(case.data)['LeaveAmount']    #获取到需要充值的金额
                self.assertEqual(float(amout),float(invest_before)-float(invest_after))
                logger.info("----数据库验证成功！！！----")
        except AssertionError as e:
            Do_Excel(contants_path.excel_dir, 4).write_excel(case.case_id + 1, resp.text, "PASS")
            logger.error("----出错了：测试的预期结果！=实际结果---")
            raise e
    @classmethod
    def tearDownClass(cls):
        logger.info("----测试后置结束----")
        cls.http_request.close()


if __name__ == '__main__':
    unittest.main()