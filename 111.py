# -*- coding: utf-8 -*-
# @File    : 111.PY
# @Date    : 2019/7/8-17:55
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com
#
# 获取质数
# t=[]
#
# for i in range(0,100):
#     for j in range(2,i):
#         if i%j==0:
#             break
#     else:
#         t.append(i)
# print(t)

# case={"mobilephone":"18607353919","amount":100}
# print(case["amount"])
import json

a='{"status":0,"code":null,"data":null,"msg":"抱歉，请先登录。"}'
print(json.loads(a)['code'])
