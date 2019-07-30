# -*- coding: utf-8 -*-
# @File    : api_request.PY
# @Date    : 2019/7/8-16:19
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import requests
from common.config import config
from common.logger import get_log
import json


logger=get_log(__name__)

#前一个返回的cookies作为后面一个请求的cookies参数传进去
class Request_api:

     def api(self,method,url,data=None,json=None,cookies=None,headers=None):
         method = method.upper()  # 全部转换成大写
         url = config.get_str("api", "pre_url") + url  # 配置文件和excel的路径拼接
         print(url)

         if type(data) == str:  # 如果data的类型是字符串，就转换成python能识别的数据类型
             data = eval(data)

         if method=="GET":
             resp=requests.get(url=url,params=data,cookies=cookies,headers=headers)

         elif method=="POST":
             if data:
                 resp=requests.post(url=url,data=data,cookies=cookies,headers=headers)
             else:
                 resp=requests.post(url=url,json=json,cookies=cookies,headers=headers)

         else:
             resp=None
             logger.error("no  this method")
         return resp



#session持久化
class Session_api:
    def __init__(self):
        self.session=requests.session()

    def api(self,method,url,data=None,json=None,headers=None):
        method = method.upper() #全部转换成大写
        url = config.get_str("api", "pre_url") + url    #配置文件和excel的路径拼接

        if type(data)==str:     #如果data的类型是字符串，就转换成python能识别的数据类型
            data=eval(data)


        if method=="GET":
            resp=self.session.request(method,url=url,params=data,headers=headers)

        elif method=="POST":
            if data:
                resp=self.session.request(method,url=url,data=data,headers=headers)
            else:
                resp=self.session.request(method,url,json=json,headers=headers)

        else:
            resp=None
            logger.error("no  this method")
        return resp

    def close(self):
        self.session.close()


if __name__ == '__main__':
    RES=Session_api().api("post","/member/register",data={"mobilephone":"18607353919","pwd":"123456"})
    print(RES.text)



