# -*- coding: utf-8 -*-
# @File    : do_mysql.PY
# @Date    : 2019/7/9-11:58
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import pymysql
from common.logger import get_log
from common.config import config

logger=get_log(__name__)

class Do_Mysql:
    def __init__(self):
        self.host=config.get_str("DB","host")
        self.user=config.get_str("DB","user")
        self.password=config.get_str("DB","password")
        self.db=config.get_str("DB","db")
        self.port = config.get_int("DB","port")
        self.charset=config.get_str("DB","charset")
        self.conn=None
        self.cur=None

    #连接数据库
    def Connect_Database(self):
       try:
           self.conn=pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.db,port=self.port,charset=self.charset)
       except:

           logger.error("connectDatabase failed")

           return False
       # self.cur=self.conn.cursor() #使用cursor()方法获取操作游标
       self.cur=self.conn.cursor(pymysql.cursors.DictCursor) #创建游标，以字典格式返回
       return True


    #获取一条数据--用来查询表数据    返回元组
    def fetch_one(self,sql):
        self.execute_sql(sql,params=None)
        self.conn.commit()
        return self.cur.fetchone()

    #获取全部数据--用来查询表数据   返回嵌套元组
    def fetch_all(self,sql):
        self.execute_sql(sql, params=None)
        self.conn.commit()
        return  self.cur.fetchall()

    #执行数据库的sql语句，主要用来做插入操作
    def execute_sql(self,sql,params=None):
        #连接数据库
        self.Connect_Database()
        try:
            if self.conn and self.cur:
                #正常逻辑。执行sql,提交操作
                self.cur.execute(sql,params)
                self.conn.commit()  #提交sql数据
        except:
            logger.error("execute failed:"+sql)
            logger.error("params:"+params)
            self.close()
            return False
        return True


    #关闭数据库
    def close(self):
        #如果数据打开，则先关闭游标后关闭数据库。否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

if __name__ == '__main__':
    sql="select LeaveAmount from future.member where MobilePhone = '18607353919'"
    RES = Do_Mysql().fetch_one(sql)
    print(RES)