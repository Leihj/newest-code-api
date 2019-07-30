# -*- coding: utf-8 -*-
# @File    : study re.PY
# @Date    : 2019/7/11-10:28
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import re
#re.match()方法匹配的是以xxx开头的字符串，若不是开头的，尽管属于str内，则无法匹配
#使用match方法进行匹配操作，匹配到的数据会被存放到result内
# result=re.match("HGS","HGS.PYTHON3")
# print(result.group())
# s='leihj_你好_186'
# p=r'(\d*)([a-zA-Z]*)'
# p=r'([1-9][0-9]{4,})'


# ret=re.match(p,s)
# print(ret.group())
# ret.group(1))


import re

d="#(.*?)#"
p='{"mobilephone":"#normal_user#","pwd":"#normal_pwd#"}'
print(re.findall(d,p))

