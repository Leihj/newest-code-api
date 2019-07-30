# -*- coding: utf-8 -*-
# @File    : test_register.PY
# @Date    : 2019/7/9-16:57
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import unittest
from common.api_request import Session_api
from common.logger import get_log
from common.do_excel import Do_Excel
from common import contants_path
from ddt import ddt,data,unpack
from common.do_mysql import Do_Mysql



logger=get_log(__name__)
@ddt
class Register_Test(unittest.TestCase):
    excel = Do_Excel(contants_path.excel_dir, 0)
    cases=excel.read_excel()


    @classmethod
    def setUpClass(cls):
        logger.info("----测试前置开始----")
        cls.http_request=Session_api()
        cls.db=Do_Mysql()
        

    @data(*cases)
    def test_success(self,case):
        logger.info("----测试用例：{}开始执行-----".format(case.title))

        if case.data.find("register_mobile")>-1:
            sql="SELECT max(mobilephone) FROM future.member  WHERE mobilephone like '1860735%';"
            mobilephone=self.db.fetch_one(sql)["max(mobilephone)"]  #返回的是字符串
            befor_mobilephone=int(mobilephone)+1  #最大手机号码或最小手机号码+1
            case.data=case.data.replace("register_mobile",str(befor_mobilephone)) #将int类型的mobilephone转成str类型的mobilephone进行字符串的替换
            logger.info("----requests----请求开始")
            resp = self.http_request.api(case.method, case.url, case.data)
            try:
                self.assertEqual(case.expected,resp.text)
                Do_Excel(contants_path.excel_dir, 0).write_excel(case.case_id+1,resp.text,"PASS")
                if resp.json()['msg']=='注册成功':
                    if case.check_sql:
                        logger.info("case.check_sql".format(case.check_sql))

                        sql=eval(case.check_sql)["sql1"]+str(befor_mobilephone)#取到excel的数据是str类型，需要用eval函数转换一下
                        print("sql",sql)
                        after_mobilephone=self.db.fetch_one(sql)['max(mobilephone)']
                        self.assertEqual(str(befor_mobilephone),after_mobilephone)  #befor_mobilephone和after_mobilephone类型一致进行对比


            except Exception as  e:
                Do_Excel(contants_path.excel_dir, 0).write_excel(case.case_id + 1,resp.text,"FAILED")
                logger.error("---测试预期结果和实际结果不一致！！---".format(e))
                raise e
            logger.info("----测试结束了----")




    @classmethod
    def tearDownClass(cls):
        logger.info("----测试后置结束----")
        cls.http_request.close()
        cls.db.close()  #连接完数据库一定要记得关闭连接


if __name__ == '__main__':
    unittest.main()