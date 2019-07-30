# -*- coding: utf-8 -*-
# @File    : re_reflect.PY
# @Date    : 2019/7/19-11:18
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

# 正则表达式和反射
import configparser
import re
from common.config import config

class Context:
    loan_id = None

    def replace(self,data):
        # data = '{"mobilephone":"#normal_user#","pwd":"#normal_pwd#"}'
        p="#(.*?)#"
        # print(re.search(p,data).group(1))

        for i in re.findall(p,data):
            s=re.findall(p,data)
            try:
                if i in s:
                    v=config.get_str("data",i)
            except configparser.NoOptionError as e:
                if hasattr(Context,i):
                    v=getattr(Context,i)
                else:
                    print("找不到参数化的值")
                    raise e
                #记得替换后的内容，一定要继续用data接收
            data=re.sub(p,v,data,count=1)   #查找和替换，count查找替换的次数
        return data
if __name__ == '__main__':

    Context().replace('{"mobilephone":"#normal_user#","pwd":"#normal_pwd#"}')



